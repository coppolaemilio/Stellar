<Sprite>spr_circle
#class
#__init__

    def event_create(self):
        <Actions>
        <AddActionComment>"This is the creation event"
        <AddActionScript>creating_script
    def event_step(self, time_passed):
        <Actions>
        <AddActionScript>step_script
