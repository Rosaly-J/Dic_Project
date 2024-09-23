import re

import pymysql
import requests


class FindWordSystem:
    def __init__(self):
        self.connection = pymysql.connect(host='localhost',
                             user='root',
                             password='oz-password',
                             db='pymysql_project',
                             charset='utf8mb4',
                             cursorclass=pymysql.cursors.DictCursor)

        # SQL 연결문

    def input_word(self, step): # self는 클래스의 인스턴스 자신을 가리킨다.
        if step == "command":
            message = "명령어를 입력해 주세요.: "
        # 단어 입력

        elif step == "search":
            message = '영어 단어를 입력해 주세요.: '
        # DB에서 단어 찾기

        elif step == "delete":
            message = '내 사전에서 삭제할 영어 단어를 입력해 주세요.'
            # DB에서 단어 삭제
        else:
            raise ValueError("invalid step")
        # 그 이외의 잘못된 명령어

        user_word = input(message)
        return user_word

    def validate_word(self, user_word): # 영어만 인식하는 기능 (특수문자 X)
        return bool(re.match(r'^[a-zA-Z]+$', user_word))


    def request_search_api(self, word):
        # url : 필요한 데이터 요청을 보낼 api url 주소
        url = f'https://api.dictionaryapi.dev/api/v2/entries/en/{word}'
        # requests 라이브러리 이용 - url로 get 요청 보냄 > 응답을 받아 response에 저장
        response = requests.get(url)  # 요청

        # status code 요청 성공 여부 확인 / 200번대 success
        if response.status_code == 200:  # status code 요청 성공 확인
            # {"key": value(int, list, dict, str, class, method)}
            # json {"key": "value"} frontend <- json data -> backend
            # response : {"key": "value"}
            # json -> dict : use .json() response.data = {"key": value, "key2": value2 ...}
            # response.json() : {"key": value(int, list, dict, str, class, method)}
            data = response.json()
            # data 변수에 response.json() 의 값이 들어있다면 -> 응답을 받았을 때 데이터가 들어있나를 판단
            if data:
                word = data[0]['word']
                meanings = data[0]['meanings'][0]['definitions'][0]['definition']
                # 튜플 형태로 데이터 저장

                return word, meanings
            else:
                print("해당 단어를 찾을 수 없습니다.")
                return None, None
            # 해당 단어를 찾을 수 없거나 오타일 시
        else:
            print(f'요청에 실패했습니다. {response.status_code}')
            return None, None
        # 요청 실패

    def save_my_dictionary(self, word, meaning): # 단어 저장하는 기능
        insert_query = "INSERT INTO my_dict (word, meaning) VALUES (%s, %s)"
        # DB속으로 단어를 저장하는 쿼리문

        with self.connection.cursor() as cursor:
            cursor.execute(insert_query, (word, meaning))
            cursor.connection.commit() # 데이터 실시간 업데이트를 위한 커밋
        if cursor.rowcount == 0:
            print(f"'{word}'는 이미 저장된 단어입니다. 중복 저장이 불가능합니다.") # 단어가 이미 DB에 있는 경우
        else:
            print(f"'{word}' 단어가 성공적으로 저장되었습니다.") # DB에 없는 경우 API에서 받아와서 저장하는 경우

    def show_my_dictionary(self): # DB에 저장된 단어 출력
        with self.connection.cursor() as cursor:
            cursor.execute("SELECT word, meaning FROM my_dict") # my_dict에서 단어 가져오기
            result = cursor.fetchall()
        i = 1
        for data in result:
            print(f"{i}. {data["word"]}의 의미 : {data["meaning"]}") # DB에 저장된 단어를 보여주는 형태
            i += 1 # 앞에 번호 인식

    def search_in_dictionary(self, word): # DB에 저장된 내 단어 찾기
        sql = "SELECT * FROM my_dict WHERE word = %s" # SQL에서 쿼리를 날려서 저장된 단어 불러오기
        with self.connection.cursor() as cursor:
            cursor.execute(sql, (word,))
            result = cursor.fetchone()
        return result

    def delete_from_dictionary(self, word): # DB에 저장된 내 단어 삭제하기
        with self.connection.cursor() as cursor:
            delete_query = "DELETE FROM my_dict WHERE word = %s" # 삭제 쿼리문
            cursor.execute(delete_query, (word,))
            cursor.connection.commit() # 데이터 실시간 업데이트를 위한 커밋
            if cursor.rowcount > 0:
                print(f"'{word}' 단어가 성공적으로 삭제되었습니다.") # 단어 있을 시 문구
            else:
                print(f"'{word}'  단어를 내 사전에서 찾을 수 없습니다.") # 단어 없을 시 문구
