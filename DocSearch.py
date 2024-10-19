import numpy as np
import math


def build_dictionary():
    # create dictionary as array
    dictionary = set()
    with open("docs.txt", "r") as corpus:
        for line in corpus:
            words = line.split()
            dictionary.update(words)

    print("Words in dictionary:", len(dictionary))

    return list(dictionary)


def build_inverted_index(dictionary):
    # create inverted index as a dictionary
    inv_index = {}
    for word in dictionary:
        inv_index[word] = set()

    with open("docs.txt", "r") as corpus:
        id = 1
        for line in corpus:
            seen_words = set()
            words = line.split()
            for word in words:
                if word not in seen_words:
                    seen_words.add(word)
                    inv_index[word].add(id)
            id += 1

    return inv_index


def search_doc():
    dictionary = build_dictionary()
    inv_index = build_inverted_index(dictionary)

    with open("queries.txt", "r") as queries:
        for line in queries:
            print("Query:", line.strip())
            query_words = line.split()
            query_vector = np.zeros(len(dictionary))
            relevant_docs = None

            for word in query_words:
                if word in dictionary:
                    word_index = dictionary.index(word)
                    query_vector[word_index] = 1
                    if relevant_docs is None:
                        relevant_docs = inv_index[word].copy()
                    else:
                        relevant_docs = relevant_docs.intersection(inv_index[word])

            if relevant_docs:
                angles = {}
                print("Relevant documents:", " ".join(map(str, sorted(relevant_docs))))
                for doc_id in relevant_docs:
                    doc_vector = build_doc_vector(doc_id, dictionary)
                    angle = calc_angle(doc_vector, query_vector)
                    angles[doc_id] = angle
                for doc_id in sorted(angles, key=angles.get):
                    print(f"{doc_id} {angles[doc_id]:.5f}")
            else:
                print("Relevant documents:")


def build_doc_vector(doc_id, dictionary):
    doc_vector = np.zeros(len(dictionary))
    with open("docs.txt", "r") as corpus:
        current_id = 1
        for line in corpus:
            if current_id == doc_id:
                words = line.split()
                for word in words:
                    word_index = dictionary.index(word)
                    doc_vector[word_index] += 1
                break
            current_id += 1

    return doc_vector


def calc_angle(x, y):
    norm_x = np.linalg.norm(x)
    norm_y = np.linalg.norm(y)
    cos_theta = np.dot(x, y) / (norm_x * norm_y)
    theta = math.degrees(math.acos(cos_theta))
    return theta


search_doc()
