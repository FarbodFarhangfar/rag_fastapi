HF_TOKEN = "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"

PROMPT = """ Using only the information contained in the context,
  answer only the question asked without adding suggestions of possible questions and answer exclusively in English.
  If the answer cannot be deduced from the context, reply: "\I don't know because it is not relevant to the Context.\"
  Context: {join(documents)};
  Question: {query}
  """