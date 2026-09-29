_updated for OJS 3.5_

# Script for batch editing article publication dates to match issue publication dates in an Open Journal System (OJS) journal

Python script developed for [York Digital Journals](https://dsi.library.yorku.ca/ydj/). Uses the [REST API for OJS 3.5](https://docs.pkp.sfu.ca/dev/api/ojs/3.5).

This script was used to batch edit the publication dates of articles to match the publication dates of the issues in which they are published. It was developed for a born-print journal's archive that was ingested to OJS. The publication dates in OJS matched the ingest dates, not the original publication dates. We wanted to correct the publication dates before registering DOIs for the articles.

At time of publishing, the OJS API does not permit PUT requests to edit issue data. Therefore, we needed to manually edit the issue publication dates via the OJS web interface to input the correct publication dates.

**Caution 1**: this script does not account for article versioning. The journal for which this was developed only uses OJS to create and disseminate the digital archive with very little input from the journal editors so no articles have multiple versions. I suspect that versioning will complicate the script when it comes to handling publication IDs.

**Caution 2**: this script assumes the article dates and issue dates should be the same. It would not work for a journal with continuous publication or forthcoming/online first.

## API endpoints and tokens

The API endpoints and tokens get coded into the file directly.
- API token as `Authorization` header
- endpoint URL: [GET list of issues](https://docs.pkp.sfu.ca/dev/api/ojs/3.5#tag/Issues/paths/~1issues/get)
- endpoint URL: [GET issue by ID](https://docs.pkp.sfu.ca/dev/api/ojs/3.5#tag/Issues/paths/~1issues~1{issueId}/get)
- endpoint URL: [PUT edit publication](https://docs.pkp.sfu.ca/dev/api/ojs/3.5#tag/Submissions-Publications/paths/~1submissions~1{submissionId}~1publications~1{publicationId}/put)

This version of the script omits 2 calls since 3.5 has restored the ability to edit publications directly without unpublishing or versioning.

The endpoint URLs include the placeholders `{issueId}`, `{submissionId}`, and `{publicationId}` used in the API reference. The script will contextually replace these with the actual IDs.

The script pulls the token and endpoint URLs by the index position and assigns them to variables.

## Process

### Get list of issues

Get a list of issues in order to extract the issue IDs. Then start a loop that iterates through each issue ID.

### Get issue by ID

Within the loop, get an issue by ID to do two things: get the publication date (and assign it to a variable) and get the submission and publication IDs for all the published articles within that issue. Then start a nested loop that iterates through each article in the issue.

### Edit

Still in the nested loop, edit 'datePublished' for the article to match the publication date for the issue.

### End of loop

Print the submission ID, publication ID, unpublish API response code, edit API response code, and published API response code for logging and debugging.

Go to the next article in the issue, or exit the nested loop if none.

Go to the next issue in the list, or exist the loop if none.
