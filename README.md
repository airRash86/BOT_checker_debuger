Телеграм бот для проверки состояния бекенда сайта 
Данный бот обслуживает сайт озвучи текста https://rashprojs.ru/voiceworker/
GITHUB сайта: github.com/airRash86/Govorilka-Voiceworker

🟣Найти работающую в продакшне версию бота по ТГ поиску: @Checker_RashProjs_bot
🟣Через адресную строку: https://t.me/Checker_RashProjs_bot
🟣GITHUB:

Идея этого бота в  том, чтобы он по графику (schedule) раз в сутки "подчищал" мп3 файлы (и записи о них в БД),
которые формируются после конвертации текста в голос (это функционал сайта озвучки: см ссылку выше).
Также этот бот, являясь членом специального ТГ канала (скриншот аватарки канала ниже, но т.к. он приватный его найти через поиск
ТГ вряд ли получится), приняв команду "TOTAL" от меня, как от оператора, которая высылается, 
как команда (ping) для всех трех ботов-членов этого канала, обсуждаемый бот 
может производить схожую проверку с той, которая производится в авто режиме ежевечерне
(и, при необходимости, также почистить бекенд сайта) и пинговать попутно код-статус отклика  этого сайта.
Вообще идеей этого канала для проверки отклика ботов объединены все, пока что (повторюсь) три, моих ТГ бота.
Не смотря на то, что все три этих ТГ бота, коды которых имеются на моем GITHUB, явл-ся "демонами" и у них есть "иммунитет" от 
"педений", тем не менее, не смотря на меры предосторожности, "падения" эти все же, изредко, но, случаются.
И как раз, чтобы пинг этих ботов был удобным и локаничным (три клика и отклик или его отстутвтеи сразу от всех 
трех ботов) и был сформирован спец канал. Боты в одном месте, одной комнадой можно проверить: онлайн ли они или "легли": быстро
и удобно) 
Данную  затею можно реализовать и через модуль TELTHON, но, все таки, я решил остановится именно на версии через канал. 

Фигурирующие в файле DEBUGER_CHECKER.py (Главный файл бота. Находится в этом репо) 
три .TXT файла ("unp_uniq_mp3", "unp_uniq_DB", "w200orNOT") - они для временного хронения данных (из кода это станет понятным).

Ну и как упоминалось выше, обсуждаемый бот имеет доступ к БД и генерируемым мп3 файлам из проекта сайта озвучки текста. 
И как и в README проекта сайта-озвучки, я пркреплю ниже скрин структуры его БД.

ℹ Деплой: реализован через размещение и запуск исполняемого файла бота на одном из vds. 


Скрин канала ботТолкинга

в ридми говорилки вставить ссылку на репо этого бота