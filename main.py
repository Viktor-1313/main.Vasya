import os
import webbrowser
from tkinter import Tk, Label, Frame, Entry, messagebox, PhotoImage, Canvas


class RoundedButton(Canvas):
    """Класс для создания закругленных кнопок"""
    def __init__(self, master=None, text="", radius=40, bg="green", fg="white",
                 active_bg="dark green", active_fg="black", command=None, font=("Arial", 14), **kwargs):
        super().__init__(master, highlightthickness=0, **kwargs)
        self.config(bg=master.cget("bg"))
        self.radius = radius
        self.bg = bg
        self.fg = fg
        self.active_bg = active_bg
        self.active_fg = active_fg
        self.command = command
        self.text = text
        self.is_active = False
        self.font = font  # Добавляем параметр шрифта
        # Обработка событий
        self.bind("<Button-1>", self._on_click)
        self.bind("<Enter>", self._on_enter)
        self.bind("<Leave>", self._on_leave)
        # Отрисовка кнопки
        self.draw_button()

    def draw_button(self):
        """Отрисовывает закругленную кнопку"""
        self.delete("all")
        width = self.winfo_reqwidth()
        height = self.winfo_reqheight()
        # Рисуем закругленный прямоугольник
        bg_color = self.active_bg if self.is_active else self.bg
        self.create_rounded_rect(0, 0, width, height, radius=self.radius, fill=bg_color, outline="")
        # Добавляем текст с использованием параметра font
        fg_color = self.active_fg if self.is_active else self.fg
        self.create_text(width // 2, height // 2, text=self.text, fill=fg_color, font=self.font)

    def _on_click(self, event):
        """Обработчик нажатия на кнопку"""
        if self.command:
            self.command()

    def _on_enter(self, event):
        """Обработчик наведения курсора"""
        self.is_active = True
        self.draw_button()  # Перерисовываем кнопку с активными цветами

    def _on_leave(self, event):
        """Обработчик ухода курсора"""
        self.is_active = False
        self.draw_button()  # Перерисовываем кнопку с исходными цветами


# Добавляем метод create_rounded_rect в Canvas
def create_rounded_rect(self, x1, y1, x2, y2, radius=40, **kwargs):
    """Создает закругленный прямоугольник на Canvas"""
    points = [
        x1 + radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1
    ]
    return self.create_polygon(points, smooth=True, **kwargs)


Canvas.create_rounded_rect = create_rounded_rect


class App(Tk):
    def __init__(self):
        super().__init__()
        self.title("Гуляй, Вася!")
        self.geometry(self.center_window(400, 830))  # Устанавливаем размеры и центрируем окно
        self.frames = {}
        self.current_frame = None
        self.images = {}  # Словарь для хранения изображений
        # Создаем папку для изображений, если её нет
        if not os.path.exists("images"):
            os.makedirs("images")
            print("Создана папка images. Поместите туда ваши изображения.")
        # Загрузка изображений
        self.load_images()
        # Создание всех фреймов
        self.create_frames()
        # Показываем начальный экран
        self.show_frame("Registration")
        # Привязка клавиши Esc к выходу из приложения
        self.bind("<Escape>", self.exit_app)

    def load_images(self):
        """Загружает все PNG изображения из папки images"""
        try:
            for filename in os.listdir("images"):
                if filename.lower().endswith(('.png', '.jpg', '.jpeg')):
                    name = os.path.splitext(filename)[0]
                    try:
                        img = PhotoImage(file=os.path.join("images", filename))
                        self.images[name] = img
                        print(f"Успешно загружено: {filename}")
                    except Exception as e:
                        print(f"Ошибка загрузки {filename}: {str(e)}")
        except Exception as e:
            print(f"Общая ошибка при загрузке изображений: {str(e)}")

    def create_frames(self):
        """Создает все фреймы приложения"""
        self.create_frame("Registration", self.create_registration_ui)
        self.create_frame("log_in_to_the_app", self.create_login_ui)
        self.create_frame("choose_a_situation", self.create_choose_a_situation_ui)
        self.create_frame("Save_me_from_my_boss", self.create_save_me_from_my_boss_ui)
        self.create_frame("required_time", self.create_required_time_ui)
        self.create_frame("I_m_not_going_to_work_on_Saturday", self.create_saturday_ui)
        self.create_frame("To_a_bar_with_friends", self.create_bar_ui)
        self.create_frame("Feedback_end", self.create_feedback_ui)
        self.create_frame("Phone_loss", self.create_phone_loss_ui)
        self.create_frame("settings", self.create_settings_ui)
        self.create_frame("Chief_scam_1", self.create_chief_scam_1_ui)
        self.create_frame("boss", self.boss_ui)


    def create_frame(self, name, setup_func):
        """Создает фрейм с указанной функцией настройки"""
        frame = Frame(self)
        self.frames[name] = frame
        setup_func(frame)

    def show_frame(self, frame_name):
        """Показывает указанный фрейм"""
        if frame_name not in self.frames:
            print(f"Фрейм {frame_name} не найден!")
            return
        if self.current_frame:
            self.current_frame.pack_forget()
        frame = self.frames[frame_name]
        frame.pack(fill="both", expand=True)
        self.current_frame = frame

    def exit_app(self, event):
        """Закрывает приложение при нажатии клавиши Esc"""
        self.destroy()

    def center_window(self, width, height):
        """Вычисляет координаты для размещения окна по центру экрана"""
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        return f"{width}x{height}+{x}+{y}"

    def create_registration_ui(self, frame):
        """Настройка UI для экрана регистрации"""
        if "Registration" in self.images:
            bg_label = Label(frame, image=self.images["Registration"])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        RoundedButton(
            frame,
            text="Регистрация",
            bg="green",
            fg="white",
            active_bg="dark green",
            active_fg="black",
            radius=25,
            command=lambda: self.show_frame("log_in_to_the_app"),
            width=300,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_login_ui(self, frame):
        """Настройка UI для входа"""
        if "log_in_to_the_app" in self.images:
            bg_label = Label(frame, image=self.images["log_in_to_the_app"])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)
        # Поле ввода телефона
        phone_entry = Entry(frame, font=("Arial", 12))
        phone_entry.place(relx=0.6, rely=0.72, anchor="center", width=165, height=15)
        # Поле ввода кода из SMS
        sms_entry = Entry(frame, font=("Arial", 12))
        sms_entry.place(relx=0.55, rely=0.78, anchor="center", width=75, height=15)
        # Функция отправки кода
        def send_sms_code():
            phone = phone_entry.get().strip()
            if not phone:
                messagebox.showerror("Ошибка", "Введите номер телефона")
            else:
                sms_entry.delete(0, "end")
                sms_entry.insert(0, "1515")  # Имитация отправки кода
                messagebox.showinfo("Успех", f"Код отправлен на номер: {phone}")

        # Кнопка отправки кода
        send_code_button = RoundedButton(
            frame,
            text="Отправить код по SMS",
            bg="green",
            fg="white",
            active_bg="dark green",
            active_fg="black",
            command=send_sms_code,
            width=200,
            height=30
        )
        send_code_button.place(relx=0.5, rely=0.82, anchor="center")

        # Кнопка "Гоу ходить"
        def validate_and_proceed():
            phone_number = phone_entry.get().strip()
            code = sms_entry.get().strip()
            if not phone_number:
                messagebox.showerror("Ошибка", "Введите номер телефона")
            elif not code:
                messagebox.showerror("Ошибка", "Введите код из SMS")
            elif code != "1515":
                messagebox.showerror("Ошибка", "Неверный код из SMS")
            else:
                self.show_frame("choose_a_situation")

        go_button = RoundedButton(
            frame,
            text="Гоу ходить",
            bg="green",
            fg="white",
            active_bg="dark green",
            active_fg="black",
            command=validate_and_proceed,
            width=350,
            height=45
        )
        go_button.place(relx=0.5, rely=0.9, anchor="center")

        # Автоматический фокус при наведении на поле ввода телефона
        def focus_phone(event):
            phone_entry.focus_set()  # Устанавливаем фокус на поле ввода телефона

        phone_entry.bind("<Enter>", focus_phone)  # Привязываем событие <Enter> к фокусу

        # Автоматический фокус при наведении на поле ввода кода из SMS
        def focus_sms(event):
            sms_entry.focus_set()  # Устанавливаем фокус на поле ввода кода из SMS

        sms_entry.bind("<Enter>", focus_sms)  # Привязываем событие <Enter> к фокусу

    def create_choose_a_situation_ui(self, frame):
        """Настройка UI выбора ситуаций"""
        if "choose_a_situation" in self.images:
            bg_label = Label(frame, image=self.images["choose_a_situation"])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Кнопка настроек (шестерёнка)
        def create_gear_button():
            gear_button = RoundedButton(
                frame,
                text="⚙️",
                bg="white",
                fg="black",
                active_bg="black",
                active_fg="white",
                radius=25,
                command=lambda: self.show_frame("settings"),
                width=20,
                height=30
            )
            gear_button.place(relx=0.1, rely=0.07, anchor="center")

        create_gear_button()

        # Кнопка "Проспал на работу"
        def create_late_for_work_button():
            late_for_work_button = RoundedButton(
                frame,
                text="Проспал на работу",
                bg="green",
                fg="white",
                active_bg="dark green",
                active_fg="black",
                radius=25,
                command=lambda: self.show_frame("Save_me_from_my_boss"),
                width=300,
                height=50
            )
            late_for_work_button.place(relx=0.5, rely=0.2, anchor="center")

        create_late_for_work_button()

        # Кнопка "Горит дедлайн"
        def create_deadline_button():
            deadline_button = RoundedButton(
                frame,
                text="Горит дедлайн",
                bg="green",
                fg="white",
                active_bg="dark green",
                active_fg="black",
                radius=25,
                command=lambda: self.show_frame("required_time"),
                width=300,
                height=50
            )
            deadline_button.place(relx=0.5, rely=0.3, anchor="center")

        create_deadline_button()

        # Кнопка "Выход в субботу"
        def create_saturday_button():
            saturday_button = RoundedButton(
                frame,
                text="Выход в субботу",
                bg="green",
                fg="white",
                active_bg="dark green",
                active_fg="black",
                radius=25,
                command=lambda: self.show_frame("I_m_not_going_to_work_on_Saturday"),
                width=300,
                height=50
            )
            saturday_button.place(relx=0.5, rely=0.4, anchor="center")

        create_saturday_button()

        # Кнопка "Гуляем с друзьями"
        def create_friends_button():
            friends_button = RoundedButton(
                frame,
                text="Гуляем с друзьями",
                bg="green",
                fg="white",
                active_bg="dark green",
                active_fg="black",
                radius=25,
                command=lambda: self.show_frame("To_a_bar_with_friends"),
                width=300,
                height=50
            )
            friends_button.place(relx=0.5, rely=0.5, anchor="center")

        create_friends_button()

        # Кнопка "Оставить отзыв"
        def create_feedback_button():
            feedback_button = RoundedButton(
                frame,
                text="Оставить отзыв",
                bg="green",
                fg="white",
                active_bg="dark green",
                active_fg="black",
                radius=25,
                command=lambda: self.show_frame("Feedback_end"),
                width=300,
                height=50
            )
            feedback_button.place(relx=0.5, rely=0.6, anchor="center")

        create_feedback_button()

        # Кнопка "создать свою карту"
        import webbrowser  # Импортируем модуль для работы с браузером

        # Кнопка "Создать свою карту"
        def create_custom_map_button():
            def open_yandex_maps():
                """Открывает Яндекс.Карты в браузере"""
                webbrowser.open("https://yandex.ru/maps/ ")

            custom_map_button = RoundedButton(
                frame,
                text="Создать свою карту",
                bg="green",
                fg="white",
                active_bg="dark green",
                active_fg="black",
                radius=25,
                command=open_yandex_maps,  # Вызываем функцию для открытия Яндекс.Карт
                width=300,
                height=50
            )
            custom_map_button.place(relx=0.5, rely=0.7, anchor="center")

        create_custom_map_button()
        # Кнопка "Потерял телефон"
        def create_phone_loss_button():
            phone_loss_button = RoundedButton(
                frame,
                text="Потерял телефон",
                bg="red",
                fg="white",
                active_bg="dark red",
                active_fg="black",
                radius=25,
                command=lambda: self.show_frame("Phone_loss"),
                width=300,
                height=50
            )
            phone_loss_button.place(relx=0.5, rely=0.9, anchor="center")

        create_phone_loss_button()
    def create_save_me_from_my_boss_ui(self, frame):
        """Экран 'Проспал на работу'"""
        if "Save_me_from_my_boss" in self.images:
            bg_label = Label(frame, image=self.images["Save_me_from_my_boss"])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)



        def create_custom_map_button():
            def open_yandex_traffic():
                """Открывает Яндекс.Пробки в браузере"""
                url = "https://yandex.ru/maps/2/saint-petersburg/probki/?ll=30.314997%2C59.938784&z=11/ "
                webbrowser.open(url)  # Открываем ссылку в браузере

            custom_map_button = RoundedButton(
                frame,
                text="Выбрать самую большую пробку",
                bg="green",
                fg="white",
                active_bg="dark green",
                active_fg="black",
                command=open_yandex_traffic,  # Вызываем функцию для открытия Яндекс.Пробок
                width=350,
                height=50
            )
            custom_map_button.place(relx=0.5, rely=0.8, anchor="center")

        create_custom_map_button()

        Label(frame, text="", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Scam",
            bg="green",
            fg="white",
            active_bg="dark green",
            active_fg="black",
            command=lambda: self.show_frame("Chief_scam_1"),
            width=350,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_chief_scam_1_ui(self, frame):
        """Настройка UI для экрана 'Chief_scam_1'"""
        if "Chief_scam_1" in self.images:
            bg_label = Label(frame, image=self.images["Chief_scam_1"])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Пример кнопки "Назад"
        RoundedButton(
            frame,
            text="←",
            bg="",
            fg="black",
            active_bg="",
            active_fg="grey",
            radius=25,
            command=lambda: self.show_frame("choose_a_situation"),
            width=30,
            height=30
        ).place(relx=0.1, rely=0.1, anchor="center")

        # Пример кнопки "Вы в пути"
        RoundedButton(
            frame,
            text="Вы в пути",
            bg="green",
            fg="white",
            active_bg="dark green",
            active_fg="black",
            radius=25,
            command=lambda: self.show_frame("boss"),
            width=150,
            height=30
        ).place(relx=0.22, rely=0.71, anchor="center")

    def boss_ui(self, frame):
        """Настройка UI для экрана 'boss'"""
        if "boss" in self.images:
            bg_label = Label(frame, image=self.images["boss"])
            bg_label.place(x=0, y=0, relwidth=1, relheight=1)

        # Пример кнопки "Назад" с уменьшенным шрифтом
        RoundedButton(
            frame,
            text="Сидим с котом за столом,"
                 "я и он, прямо в субботу",
            bg="green",
            fg="white",
            active_bg="dark green",
            active_fg="black",
            radius=25,
            command=lambda: self.show_frame("choose_a_situation"),
            width=370,
            height=50,
            font=("Arial", 12)  # Уменьшаем размер шрифта до 10 для этой кнопки
        ).place(relx=0.5, rely=0.7, anchor="center")

    def create_required_time_ui(self, frame):
        """Экран 'Горит дедлайн'"""
        Label(frame, text="Горит дедлайн", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_saturday_ui(self, frame):
        """Экран 'Выход в субботу'"""
        Label(frame, text="Выход в субботу", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_bar_ui(self, frame):
        """Экран 'Гуляем с друзьями'"""
        Label(frame, text="Гуляем с друзьями", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_feedback_ui(self, frame):
        """Экран 'Оставить отзыв'"""
        Label(frame, text="Оставить отзыв", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_phone_loss_ui(self, frame):
        """Экран 'Потерял телефон'"""
        Label(frame, text="Потерял телефон", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")

    def create_settings_ui(self, frame):
        """Экран 'Настройки'"""
        Label(frame, text="Настройки", font=("Arial", 20)).place(relx=0.5, rely=0.1, anchor="center")
        RoundedButton(
            frame,
            text="Назад",
            bg="blue",
            fg="white",
            active_bg="dark blue",
            active_fg="black",
            command=lambda: self.show_frame("choose_a_situation"),
            width=200,
            height=50
        ).place(relx=0.5, rely=0.9, anchor="center")


if __name__ == "__main__":
    app = App()
    app.mainloop()