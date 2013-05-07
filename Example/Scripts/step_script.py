# Limit the circles to inside the room.
if sge.get_key_pressed('right') :
    self.x+=self.velocidad
if sge.get_key_pressed('left') :
    self.x-=self.velocidad
if sge.get_key_pressed('down') :
    self.y+=self.velocidad
if sge.get_key_pressed('up') :
    self.y-=self.velocidad

for obj in sge.game.current_room.objects:
            if (obj is not self and isinstance(obj, obj_cristal) and self.collides(obj)):
                obj.destroy()
		sge.StellarClass.create(obj_cristal, 32,32)
                break