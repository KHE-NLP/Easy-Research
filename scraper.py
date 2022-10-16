import http.client
import zipfile

from parsers import get_pptx_slides

base = "antares.cs.kent.edu"
req = "/~seminar/"
if __name__ == "__main__":
    conn = http.client.HTTPConnection(base)
    conn.request("GET", req)
    data = conn.getresponse().read()
    # print(data)
    data = data.decode("utf-8")

    fl = open("train_data/summary_title.txt", "w")
    for line in data.split("\n"):
        if "<p><b>" not in line:
            continue

        parts = line.split("<a href=\"")[1:]
        urls = [sub.split("\"")[0].replace(" ", "_") for sub in parts]

        if len(urls) != 2:
            continue
        if ".pptx" not in urls[1]:
            continue

        if "abs" in urls[0]:
            urls[0] = urls[0].replace("abs", "pdf")

        if "pdf" not in urls[0]:
            continue

        try:
            slides = get_pptx_slides(urls[1], ask_desc=False)
        except zipfile.BadZipFile:
            continue

        for slide in slides:
            if len(slide) < 4:
                continue
            title = slide.split("\n")[0]
            lines = "\n".join(slide.split("\n")[1:])
            fl.write("SUMMARY:\n")
            fl.write(lines + "\n")
            fl.write("TITLE:\n")
            fl.write(title + "\n")
