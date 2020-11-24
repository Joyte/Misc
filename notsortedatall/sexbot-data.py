def dad_match(match_string):
    regex_string = r"(?:i(?:'m )?(?:(?<!'m )m )?(?:(?<!m ) am )?(?:(?<!i)))(.*)"
    import re
    return re.search(regex_string, match_string, re.IGNORECASE)


def main():
    matchlist = []
    for string in teststrings:
        match_hm = match(string)
        matchlist.append((match_hm, string))

    print(matchlist)

    for string in matchlist:
        print(string[0].groups())


if __name__ == '__main__':
    main()