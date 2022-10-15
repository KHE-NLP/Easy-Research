import http.client

base = "antares.cs.kent.edu"
req = "/~seminar/"
if __name__ == "__main__":
    conn = http.client.HTTPConnection(base)
    conn.request("GET", req)
    data = conn.getresponse().read()
    # print(data)
    data = data.decode("utf-8")

    counter = 0
    for line in data.split("\n"):
        if "<p><b>" not in line:
            continue

        parts = line.split("<a href=\"")[1:]
        urls = [sub.split("\"")[0].replace(" ", "_") for sub in parts]

        if len(urls) != 2:
            continue
        if ".ppt" not in urls[1]:
            continue

        if "abs" in urls[0]:
            urls[0] = urls[0].replace("abs", "pdf")

        if "pdf" not in urls[0]:
            continue

        print(urls)
