import bs4 as bs
import urllib.request
import pandas as pd

SNEAK_START_YEAR = 1995
SCRAPE_TO_YEAR = 2024
MYSNEAK_HISTORY_MAIN_URL = "https://mysneak.de/moviearc.php?mysndoc=mov"



def sneak_movie_selector(tag):
	return tag.name == "td" and tag.has_attr("class") and ("movtitle" in tag.get("class")  or "movdate" in tag.get("class"))

def append_row(df, row):
    return pd.concat([
                df,
                pd.DataFrame([row], columns=row.index)]
           ).reset_index(drop=True)


def main():
    df = pd.DataFrame(columns=('sneak_nr', 'sneak_date', 'movie_title'))

    for sneak_year in range(SNEAK_START_YEAR, SCRAPE_TO_YEAR + 1):
        histroy_page = urllib.request.urlopen(f'{MYSNEAK_HISTORY_MAIN_URL}{sneak_year}').read()
        soup = bs.BeautifulSoup(histroy_page,'lxml')
        results_of_year = soup.find_all(sneak_movie_selector)



        sneak_nr = ""
        sneak_date = ""
        movietitle = ""

        order = True
        for idx, result in enumerate(results_of_year, start=1):
            content = result.contents[0]


            if idx % 2 == (1 if order else 0):
                splits = content.split(" ", 1)
                sneak_nr = splits[0]
                try:
                    sneak_date = f' {splits[1]} {sneak_year}'
                except:
                    # this is an invalid sneak
                    order = not order
                    continue


            if idx % 2 == (0 if order else 1):
                movietitle = content.replace('"', '').replace('\n', '')
                new_row = pd.Series({'sneak_nr':sneak_nr, 'sneak_date':sneak_date, 'movie_title': movietitle})

                df = append_row(df, new_row)


    print(df)
    df.to_csv("out.csv", encoding='utf-8')



if __name__ == "__main__":
    main()
