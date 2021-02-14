import datetime
import logging
import os, json, time
import azure.functions as func
from azure.core.exceptions import ResourceNotFoundError
from azure.storage.blob import BlobClient, BlobServiceClient
from azure.identity import DefaultAzureCredential
import yfinance as yf

def createBlobName(ticker, date_str, extension=".txt"):
        return "-".join([ticker, date_str])+extension

def getCurrClose(ticker):
    tck = yf.Ticker(ticker); 
    hist = tck.history(period="1d")
    ret =  hist['Close'][0]
    return f"{ret:.02f}"

def main(mytimer: func.TimerRequest) -> None:
    storageName = os.getenv("STORAGE_ACCOUNT_NAME")
    containerName = os.getenv("BLOB_CONTAINER_NAME")
    
    logging.info(f"params: {storageName}, {containerName}")
    ts = datetime.datetime.now()
    iso_ts = ts.isoformat()
    date_str = ts.strftime("%Y%m%d")

    credential = DefaultAzureCredential()
    oauth_url = f"https://{storageName}.blob.core.windows.net"
    
    bsc = BlobServiceClient(account_url=oauth_url, credential=credential)
    containerClient = bsc.get_container_client(containerName)
    
    tickers = ["BTC-USD", "MSFT"]
    n = len(tickers)
    for i in range(n):
        block = ",\n"
        ticker = tickers[i]
        logging.info(f"storing {ticker}")

        blobName = createBlobName(ticker, date_str)
        logging.info(f"container: {containerName}, blob: {blobName}")

        blobClient = containerClient.get_blob_client(blobName)
        try:
            if not blobClient.exists():
                blobClient.create_append_blob()
                block = ""

        except ResourceNotFoundError:
            logging.info(f"Creating container: {containerName}")
            containerClient = bsc.create_container(containerName)
            blobClient = containerClient.get_blob_client(blobName)
            blobClient.create_append_blob()
                    
        block += json.dumps({"ts": iso_ts, "v": getCurrClose(ticker)})
        
        blobClient.append_block(block)
        if i<n-1: time.sleep(1)
    
    #if mytimer.past_due:
    #    logging.info('The timer is past due!')

    
