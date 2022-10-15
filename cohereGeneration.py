import cohere
co = cohere.Client('hpaaYCC1MGPwyigl9JhSQg3NCZaLzDkSrYM6Iy6U')
responses = "Format: Title:, Author(s): Summarize the following passage for a presentation: \n ${} \n\n  Summary:"

stopsequences = ['\n\n', '\t']
response = co.generate(prompt=responses[0], max_tokens=150, temperature=0.9, k=10)
print(response.generations[0].text)
	
