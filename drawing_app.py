"""
Проект предназначен для создания изображений на основе стандартной библиотеки Tkinter.
Пользователь может рисовать на холсте, выбирать цвет и размер кисти, очищать холст и сохранять в формате PNG.
Программа состоит из одного модуля, включающего в себя класс DrawingApp

Конструктор данного класса принимает один параметр root: это корневой виджет Tkinter,
который служит контейнером для всего интерфейса приложения.
"""

import tkinter as tk
from tkinter import colorchooser, filedialog, messagebox
from PIL import Image, ImageDraw


class DrawingApp:

    def __init__(self, root):
        """
        Конструктор класса, внутри которого выполняются следующие ключевые действия:
        - устанавливается заголовок окна приложения;
        - создается объект изображения (self.image). Это изображение служит виртуальным холстом,
        на котором происходит рисование. Изначально оно заполнено белым цветом;
        - инициализируется объект ImageDraw.Draw(self.image), который позволяет рисовать на объекте изображения;
        - создается виджет Canvas Tkinter, который отображает графический интерфейс для рисования.
        Размеры холста установлены в 600x400 пикселей;
        - вызывается метод self.setup_ui(), который настраивает элементы управления интерфейса;
        - привязываются обработчики событий к холсту для отслеживания движений мыши при рисовании, и сброса состояния
        кисти при отпускании кнопки мыши.

        """
        self.root = root
        self.root.title("Рисовалка с сохранением в PNG")

        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

        self.canvas = tk.Canvas(root, width=600, height=400, bg='white')
        self.canvas.pack()

        self.setup_ui()

        self.last_x, self.last_y = None, None

        # Начальный цвет кисти
        self.pen_color = 'black'

        # Хранение предыдущего цвета кисти
        self.previous_color = self.pen_color

        # Установка начального размера кисти
        self.brush_size = 1

        self.canvas.bind('<B1-Motion>', self.paint)
        self.canvas.bind('<ButtonRelease-1>', self.reset)

        # Привязка правой кнопки мыши к методу pick_color
        self.canvas.bind('<Button-3>', self.pick_color)

    def setup_ui(self):
        """
        Этот метод отвечает за создание и расположение виджетов управления.
        Описание:
        control_frame: рамка для размещения элементов управления и добавляем её в главное меню;
        clear_button: кнопка для очистки холста. Она связана с методом clear_canvas;
        color_button: кнопка для выбора цвета. Связана с методом choose_color;
        save_button: кнопка для сохранения изображения. Связана с методом save_image;
        eraser_button: кнопка "ластик" для стирания части изображения. Связана с методом use_eraser;
        sizes: список предустановленных размеров кисти;
        self.brush_size_var: установка начального значения для размера кисти с помощью переменной типа StringVar;
        brush_size_menu: создаем выпадающий список для выбора размера кисти, который обновляет размер кисти при выборе.
        """
        control_frame = tk.Frame(self.root)
        control_frame.pack(fill=tk.X)

        clear_button = tk.Button(control_frame, text="Очистить", command=self.clear_canvas)
        clear_button.pack(side=tk.LEFT)

        color_button = tk.Button(control_frame, text="Выбрать цвет", command=self.choose_color)
        color_button.pack(side=tk.LEFT)

        save_button = tk.Button(control_frame, text="Сохранить", command=self.save_image)
        save_button.pack(side=tk.LEFT)

        eraser_button = tk.Button(control_frame, text="Ластик", command=self.use_eraser)
        eraser_button.pack(side=tk.LEFT)

        sizes = [1, 2, 5, 10]

        self.brush_size_var = tk.StringVar(value=sizes[0])
        brush_size_menu = tk.OptionMenu(
            control_frame, self.brush_size_var, *sizes, command=self.update_brush_size)
        brush_size_menu.pack(side=tk.LEFT)

    def update_brush_size(self, selected_size):
        """
        Функция update_brush_size предназначена для обновления текущего размера кисти в приложении рисования.
        Этот размер используется при рисовании линий на холсте.
        Параметр selected_size: это значение, которое передается функции при выборе размера кисти из выпадающего списка.
        Оно приходит в виде строки (string). Значение selected_size преобразуется в целое число с помощью int(),
        а затем сохраняется в атрибуте self.brush_size.
        Это позволяет программе использовать новое значение размера кисти при рисовании.
        """
        self.brush_size = int(selected_size)

    def paint(self, event):
        """
        Вызывается при движении мыши с нажатой левой кнопкой по холсту. Она рисует линии на холсте Tkinter
        и параллельно на объекте Image из Pillow.
        Описание:
        - условный оператор if: проверяем, есть ли предыдущие координаты (last_x и last_y), чтобы начать рисование линии.
        Если они существуют, это означает, что пользователь уже начал рисовать и мы можем провести линию.
        - вызов create_line: создает линию на виджете canvas. Параметры управления (width, fill, capstyle и smooth)
        определяют внешний вид линии (толщину, цвет и стиль концов)
        - self.draw.line: рисует ту же линию на объекте Image, чтобы сохранить данные для будущего сохранения в файл.
        Это необходимо, чтобы линия отображалась не только на холсте, но и была частью изображения, которое мы можем сохранить;
        - после рисования линии обновляем координаты last_x и last_y текущими координатами события.
        Это позволяет продолжать рисование, используя новые координаты как начало следующей линии.
        """
        if self.last_x and self.last_y:
            self.canvas.create_line(self.last_x, self.last_y, event.x, event.y,
                                    width=self.brush_size, fill=self.pen_color,
                                    capstyle=tk.ROUND, smooth=tk.TRUE)
            self.draw.line([self.last_x, self.last_y, event.x, event.y], fill=self.pen_color,
                           width=self.brush_size)

        self.last_x = event.x
        self.last_y = event.y

    def reset(self, event):
        """
        Этот метод сбрасывает последние координаты кисти. Это необходимо для корректного начала новой линии после того,
        как пользователь отпустил кнопку мыши и снова начал рисовать.
        """
        self.last_x, self.last_y = None, None

    def clear_canvas(self):
        """
        Очищает холст, удаляя все нарисованное, и пересоздает объекты Image и ImageDraw для нового изображения
        """
        self.canvas.delete("all")
        self.image = Image.new("RGB", (600, 400), "white")
        self.draw = ImageDraw.Draw(self.image)

    def choose_color(self):
        """
        Функция открывает стандартное диалоговое окно выбора цвета и устанавливает выбранный цвет как текущий для кисти.
        Метод colorchooser.askcolor() открывает диалоговое окно выбора цвета.
        Он принимает параметр, который задает начальный цвет (в данном случае это текущий цвет кисти self.pen_color).
        """
        self.pen_color = colorchooser.askcolor(color=self.pen_color)[1]

    def use_eraser(self):
        """
        Переключает цвет кисти на цвет фона (белый) для использования в качестве ластика.
        Сохраняем текущий цвет в переменную self.previous_color, а затем изменяем цвет кисти на белый.
        """
        self.previous_color = self.pen_color
        self.pen_color = 'white'

    def pick_color(self, event):
        """
        Этот метод позволяет пользователю выбрать цвет с помощью пипетки.
        При нажатии правой кнопки мыши на холсте берется цвет пикселя из текущих координат курсора,
        и устанавливается как цвет кисти
        Описание метода:
        - получаем координаты курсора (event.x, event.y);
        - проверяем, находится ли курсор в пределах холста;
        - получаем цвета пикселя;
        - преобразуем RGB цвет в HEX формат (рекомендовано при работе с Tkinter);
        - выводим код цвета в консоль (для отладки)
        """
        x, y = event.x, event.y
        if 0 <= x < 600 and 0 <= y < 400:
            color = self.image.getpixel((x, y))
            self.pen_color = f'#{color[0]:02x}{color[1]:02x}{color[2]:02x}'

            print(f"Выбранный цвет: {self.pen_color}")

    def save_image(self):
        """
        Позволяет пользователю сохранить изображение, используя стандартное диалоговое окно для сохранения файла.
        Поддерживает только формат PNG. В случае успешного сохранения выводится сообщение об успешном сохранении.
        """
        file_path = filedialog.asksaveasfilename(filetypes=[('PNG files', '*.png')])
        if file_path:
            if not file_path.endswith('.png'):
                file_path += '.png'
            self.image.save(file_path)
            messagebox.showinfo("Информация", "Изображение успешно сохранено!")


def main():
    root = tk.Tk()
    app = DrawingApp(root)
    root.mainloop()


if __name__ == "__main__":
    main()
