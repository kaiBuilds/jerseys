# Jerseys

A simple Streamlit application to showcase how you could use LLMs as a substitute for some complex functions provided you normalise the output ("working with agents").

Here the LLM is just put in place of a parameter sampler instead of a hand-written probabilistic generative model or some "creativity" generator (that could have parts that are neural networks but not necessarily LLMs).

Of course, this approach has downsides as well, perhaps the most obvious one is that you lose control over what you're sampling over and you just rely  on the emergent properties of LLMs to reproduce things that are "reasonable" (which is also the biggest pro of this approach).

# Other typical readme information
To be included later with the design assumptions and project observations such as
- due to laziness it still is a single codebase for something that clearly has a frontend and a backend and these should as much as possible be separate for security reasons
- more tests are needed, and possibly it'd be interesting to update the LLM querying on Azure (Also to include other endpoints like GCP)
- include all CI/CD setup for it
- etc...

(it will come eventually, but as a short side project it has low priority in my life)