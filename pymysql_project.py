from find_word_system4 import FindWordSystem

# FindWordSystem Class를 인스턴스화 -> 객체화
find_word = FindWordSystem()

# 반복문 실행
while True:
    command = find_word.input_word("command").lower()
    if command == "exit":
        print("프로그램을 종료합니다.")
        break

    elif command == "show":
        find_word.show_my_dictionary()

    elif command == "search":
        search_word = find_word.input_word("search")

        if not find_word.validate_word(search_word):
            print("영어만 입력해야 합니다. 다시입력해주세요.")
            continue

        result = find_word.search_in_dictionary(search_word)

        if result:
            print(f"'{result["word"]}'의 의미 : {result["meaning"]}")
            continue

        search_word, meaning = find_word.request_search_api(search_word)

        if search_word is None or meaning is None:
            print('입력하신 단어의 검색 결과를 가져오지 못했습니다. 다시 입력하거나 단어를 추가해주세요.')
            continue
        print(f"'{search_word}'의 의미 : {meaning}")

        find_word.save_my_dictionary(search_word, meaning)

    elif command == "delete":
        delete_word = find_word.input_word("delete")

        if not find_word.validate_word(delete_word):
            print("영어만 입력해야 합니다. 다시입력해주세요.")

        find_word.delete_from_dictionary(delete_word)

    else:
        print("잘못된 명령어 입니다. 다시 입력해주세요.")