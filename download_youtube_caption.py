# -*- coding: utf-8 -*-

# See instructions for running these code samples locally:
# https://developers.google.com/explorer-help/guides/code_samples#python

import io
import os
import json

import google_auth_oauthlib.flow
import googleapiclient.discovery
import googleapiclient.errors

from googleapiclient.http import MediaIoBaseDownload

scopes = ["https://www.googleapis.com/auth/youtube.force-ssl"]

def main():
    # Disable OAuthlib's HTTPS verification when running locally.
    # *DO NOT* leave this option enabled in production.
    os.environ["OAUTHLIB_INSECURE_TRANSPORT"] = "1"

    api_service_name = "youtube"
    api_version = "v3"
    client_secrets_file = "client_secret.json"

    # Get credentials and create an API client
    flow = google_auth_oauthlib.flow.InstalledAppFlow.from_client_secrets_file(
        client_secrets_file, scopes)
    credentials = flow.run_console()
    youtube = googleapiclient.discovery.build(
        api_service_name, api_version, credentials=credentials)

    request_list = youtube.captions().list(
        part="snippet",
        videoId="NkDEaVOJhpE"
    )
    response_list = request_list.execute()

    with open("response_list.json", "w") as f:
        f.write(json.dumps(response_list, indent=2))

    for item in response_list["items"]:
        id = item["id"]
        request_caption = youtube.captions().download(
            id=id,
            tfmt="ttml"
        )

        fh = io.FileIO(f"response_caption_{id}.ttml", "wb")

        download = MediaIoBaseDownload(fh, request_caption)
        complete = False
        while not complete:
            status, complete = download.next_chunk()


if __name__ == "__main__":
    main()