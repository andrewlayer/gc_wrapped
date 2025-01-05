# Group Chat Wrapped

## Overview

Group Chat wrapped is a project written in Python to help me make fun of my friends.  I hope it helps you make fun of your friends too.  At the moment, its not very good, but I will keep trying to make it better.  If you have any fun analysis ideas, feel free to contribute them, or leave the idea in the issues section.

This project was designed a little bit like a domain specific language. You can write the analysis that you want to in `main.py` in whatever order you want to produce the visuals, and the report will be generated in the same order. 

Note: This project will send all your data to OpenAI.  If you are concerned about privacy, please do not use this project (or use [local-ai](https://localai.io/) like me to host models locally)

## Currently Supported Analysis

- **Message Cadence Visualization**: Which of you friends is the most active over time?
- **Cluster Analysis**: Uses embeddings to group messages into clusters and provides AI-generated summaries.  It also picks out the most interesting messages from each cluster.
- **Profanity Statistics**: Which of you friends is the most profane? This should help you find out.

# Planned Features
- [ ] TODO (lol)

## Installation

1. **Install Dependencies**:
`pip install -r requirements.txt`

2. **Set Up Environment Values**:
Copy `example.env` to `.env` and fill in the required environment variables, such as `OPENAI_API_KEY`.

3. **Create Contact Map**:
Create `contact_map.json` with the correct mappings of contact identifiers to names.  You can use the `contact_map.example.json` as a starting point.  This will map the contact identifiers to the names of the people in the chat.  You **must** map `'Me'` to your name, and your email and phone number for the project to work.

4. **Get Chat Data**:
- Open Finder and hit `CMD + SHIFT + G`
- Navigate to `~/Library/Messages/chat.db` or wherever your messages app is stored.
- Duplicate the `chat.db` file and paste it into the root of this project.

5. **Run the Analysis**:
This can take a while depending on the size of your chat history.  My project with 22k messages took about 5 minutes to run.

## Code Structure

```
.
├── GroupChatWrapped.pdf
├── README.md
├── analysis
│   ├── embedding_analysis.py
│   ├── sentiment_analysis.py
│   └── timeseries_analysis.py
│   └── reaction_analysis.py
├── helpers
│   ├── clients.py
│   ├── coverage_check.py
│   ├── db.py
│   ├── dump_schema.py
│   ├── pdf_report.py
│   └── utils.py
├── main.py
└── visuals
    ├── clusters.py
    ├── message_cadence.py
    └── sentiments.py
    └── reactions.py
```

- **`main.py`**: Entry point for running the analysis and generating the report.
- **`visuals/`**: All visuals should generate a matplotlib figure.
- **`analysis/`**: Analysis files all end with analysis.py. They should generate datastructure that can be easily used by the visuals.

## Contributing

Contributions are welcome! Please fork the repository and submit a pull request for any improvements or bug fixes.

## License

This project is licensed under the MIT License.

## Acknowledgments

- Uses OpenAI's API for embedding and clustering analysis.
- Built with Python and popular data science libraries like Pandas and Matplotlib.
