layers = (sge.BackgroundLayer(fence_sprite, 0, 380, 0, yrepeat=True),)
background = sge.Background(layers, 0xffffff)

circle = obj_cristal(game.width // 2, game.height // 2)
circle1= obj_cancel(20,20)
objects = [circle,circle1]


views = (sge.View(0, 0),)

rm_0 = sge.Room(tuple(objects), views=views, background=background)
