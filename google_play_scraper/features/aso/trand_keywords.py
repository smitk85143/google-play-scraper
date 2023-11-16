from google_play_scraper.features.suggest_keyword import suggest_keyword


def tread_keywords(keyword, hl, gl):

    try:

        suggests = suggest_keyword(keyword, lang=hl, country=gl)
        suggests.pop(0)
        list1 = []
        map = {}
        map_popularity = {}

        map[keyword] = True
        map_popularity[keyword] = 100

        minus = 0
        for s in suggests:
            list1.append(s)
            map[s] = False
            map_popularity[s] = 100 - minus
            minus += 2

        def google_suggests(lst, level):

            res = []
            for sug in lst:
        
                if map.get(sug, False) == False:
                    suggests = suggest_keyword(sug, lang=hl, country=gl)
                    suggests.pop(0)
                    map[sug] = True

                    minus = 0
                    for s in suggests:
                        if map.get(s, None) == None:
                            res.append(s)
                            map[s] = False
                            if map_popularity.get(s, None) == None:
                                map_popularity[s] = level - minus
                        minus += 2   

            return res

        list2 = google_suggests(list1, 70)
        list3 = google_suggests(list2, 50)
        list4 = google_suggests(list3, 20)
        # list5 = google_suggests(list4, 15)

        data = []

        for item in map_popularity.items():
            data.append({"Key phrase": item[0], "Relative popularity": item[1]})

        data = sorted(data, key=lambda k: k['Relative popularity'], reverse=True)

        return data
    except Exception as e:
        return {"error": str(e)}