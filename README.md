<div id="header" align="center">
  <img src="https://media0.giphy.com/media/gh0RRgkTXedvF0pDc0/200.webp?cid=ecf05e47t754m7xu7dho35wtz6peo0tgq1cdki13wkcytklb&rid=200.webp&ct=g" width="300"/>
</div>
	
	
	Дипломный проект по курсу PYthon Basic.
	Подготовил: Арсентьев А.В.

Описание дирректорий и файлов:

1.Дирректория config_data хранит в себе названия основных
команд и их описание.

2.Дирректория database хранит в себе скрипт для реализации 
команд "/history". Скрипт из файла models.py отвечает за
содание класса History, являющегося базовой моделью для создания 
базы данных с историей поиска отелей.

3.Дирректория handlers хранит в себе три дирректории:
	1.Custom_handlers хранит в себе файлы со сценариями для 
	  основных команд: "/bestdeal", "/highprice", "/lowprice"
          в файлах с соответствующими названиями.
	2.Default_handlers - дирректория с файлами для описания
	  стандартных команд бота: "/start", "/help", "/echo"
	3.work_with_api - дирректория для хранения скриптов для
	  работы с API. В файле result_info.py прописан код 
	  для подключения к API, поиска отелей по заданным параметрам 
	  и вывода пользовтелю медиагруппы.
	  В файле request.py прописан код с параметрами подключения
	  к API.

4.Дирректория keyboards отвечает за созданные в боте клавиатуры.
В моем проекте использовалась Inline клавиатура для отображения 
точной локации в городе. Хранится в дирректории keybords/reply в 
файле location.py

5.Дирректория states отвечает за состаяния прользователя при
прохождении сценария опроса параметров отеля.
В файле required_info.py прописаны классы для кадой команды.
Для команды "/bestdeal" - класс UserInfoBest.
Для команд "/highprice", "/lowprice" - класс UserInfoBest.
В каждом классе прописаны состояния, необходимые для дальнейшего поиска
отелей по заданным пользователем критериям. 

6.В файле .env.template хранится информация о токене бота и ключе для
  подключения к API

7.Бот запускается из файла main.py 
