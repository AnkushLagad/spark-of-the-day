# Spark of the Day

Spark of the Day is a small story-making project. A Python program asks an AI
model on Amazon Bedrock to write a short, whimsical story. A simple website
then displays that story with its theme and an animated Three.js background.

## The inspiration

This project is inspired by the idea of autonomous AI agents: software that
can take on a small task and complete it. Projects such as Dots by OpenAI are
part of that inspiration. Spark of the Day is an independent project; it is
not made by, connected to, or endorsed by OpenAI.

## What it does

- Picks a story idea from a list of themes.
- Sends the idea to an Amazon Bedrock model that you choose.
- Saves the story and theme in `site/latest.json`.
- Saves a dated copy in `site/archive/`.
- Shows the latest story on a mobile-friendly webpage.
- Adds a decorative animated scene using Three.js. The page still works if
  the animation cannot load.

The story generator runs when you start it; it is not scheduled to run
automatically every day.

## What you need

- Python 3.9 or newer.
- An AWS account with access to an Amazon Bedrock text model.
- AWS credentials and an AWS region configured for boto3.
- Internet access for the website's Google Fonts and Three.js CDN assets.

There is no Node.js build step.

## Set it up

Install boto3, the Python package used to call AWS:

```bash
python -m pip install boto3
```

Set up AWS credentials using an AWS profile, environment variables, or
`aws configure`. Choose a Bedrock model that is enabled for your account and
region, then set its model ID in the `MODEL_ID` environment variable.

In PowerShell:

```powershell
$env:MODEL_ID = "your-enabled-bedrock-model-id"
python agent.py
```

In macOS or Linux:

```bash
export MODEL_ID="your-enabled-bedrock-model-id"
python agent.py
```

The AWS identity you use must be allowed to invoke that Bedrock model (for
example, it needs `bedrock:InvokeModel` permission). Bedrock usage may incur
charges under your AWS account. The script reports an error if `MODEL_ID` is
not set.

## View the website

After generating a story, start a local web server from the project folder:

```bash
python -m http.server 8000 --directory site
```

Visit <http://localhost:8000> in your browser. The website reads
`site/latest.json`, so run `python agent.py` whenever you want to generate a
new story. Use a local web server instead of opening `index.html` directly;
the browser needs the server to load the JSON file.

## How the parts fit together

1. `agent.py` chooses one of the story themes.
2. It asks Amazon Bedrock to write a short story about that theme.
3. It saves the result in JSON: the date, theme, and story text.
4. `site/index.html` loads that JSON and displays it. Three.js adds the
   animated background in the browser.

Your AWS credentials stay on the computer running `agent.py`. They are not
sent to the website, and the website does not call Amazon Bedrock.

## Project files

```text
.
├── agent.py                 # Creates stories with Amazon Bedrock
├── README.md                # Project guide
└── site/
    ├── index.html           # Website and Three.js background
    ├── latest.json          # Story shown on the website
    └── archive/
        └── YYYY-MM-DD.json  # Saved story by date
```
