import pickle 


file_path = r'/home/mike-pi/Documents/coding/projects/disp/data/daily_list.pkl'

if input('Внимание! Дальнейшее исполнение этого файла приведет к утрате ваших предыдущих данных!\n\
         Вы действительно хотите продолжить? Yes/no') == 'Yes':
    if input('Пожалуйста, напечатайте "Я действительно желаю продолжить"') == "Я действительно желаю продолжить":
        daily_list = []
        pickle.dump(daily_list, open(file_path, 'wb'))
