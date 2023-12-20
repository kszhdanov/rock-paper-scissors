from controller import Controller
from model import Model
from view import View


if __name__ == '__main__':
    model = Model()
    view = View(model)
    controller = Controller(model)
    model.notify()
    controller.start_infinite_cycle()
