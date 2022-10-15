import cohere

if __name__ == "__main__":
    co = cohere.Client('hpaaYCC1MGPwyigl9JhSQg3NCZaLzDkSrYM6Iy6U')
    response = co.generate(prompt='Once upon a time in a magical land called')

    print('Prediction: {}'.format(response.generations[0].text))
