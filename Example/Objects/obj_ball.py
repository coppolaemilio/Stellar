class obj_ball(sge.StellarClass):
    def __init__(self, x, y, player=0):
        super(obj_ball, self).__init__(x, y, 5, 'circle', collision_precise=True)
        self.player = player

    def event_create(self):
        <Actions>
        <AddActionComment>"This is the creation event"
        <AddActionScript>creating_script
    def event_step(self, time_passed):
        <Actions>
        <AddActionScript>step_script
