from base_character import Character


class Medusa(Character):

    def __init__(self, x, y, side, screen):
        super(Medusa, self).__init__('Medusa', x, y, 243, 197, 270, 187, 80, 1.8, 6, 9, 100,
                                     'Fantasy Free Game Kit/Characters/Monster - Medusa/PNG/FW_Meduza_Running__',
                                     'Fantasy Free Game Kit/Characters/Monster - Medusa/PNG/FW_Meduza_Attack__',
                                     side, 23, 23, screen)


class Wizard(Character):

    def __init__(self, x, y, side, screen):
        super(Wizard, self).__init__('Wizard', x, y, 148, 196, 180, 207, 70, 1.6, 5, 6, 100,
                                     'Fantasy Free Game Kit/Characters/Hero - Wizard/PNG/FW_Hero_1_Walking__',
                                     'Fantasy Free Game Kit/Characters/Hero - Wizard/PNG/FW_Hero_1_Attack__',
                                     side, 23, 8, screen)


class Minotaur(Character):

    def __init__(self, x, y, side, screen):
        super(Minotaur, self).__init__('Minotaur', x, y, 300, 234, 420, 505, 100, 3.0, 5, 8, 100,
                                       'Fantasy Free Game Kit/Characters/Monster - Minotaur/PNG/FW_Minotaur_Walking__',
                                       'Fantasy Free Game Kit/Characters/Monster - Minotaur/PNG/FW_Minotaur_Attacking__'
                                       , side, 35, 9, screen)


class Skeleton(Character):

    def __init__(self, x, y, side, screen):
        super(Skeleton, self).__init__('Skeleton', x, y, 146, 206, 193, 235, 50, 1.8, 4, 11, 100,
                                       'Fantasy Free Game Kit/Characters/Monster - Skeleton/PNG/FW_Skeleton_Walking__',
                                       'Fantasy Free Game Kit/Characters/Monster - Skeleton/PNG/FW_Skeleton_Attack__',
                                       side, 23, 19, screen)


class Golem(Character):

    def __init__(self, x, y, side, screen):
        super(Golem, self).__init__('Golem', x, y, 150, 150, 150, 150, 40, 1.3, 3, 8, 100,
                                    'Golem/Golem_1/PNG/PNG Sequences/Walking/0_Golem_Walking_',
                                    'Golem/Golem_1/PNG/PNG Sequences/Slashing/0_Golem_Slashing_',
                                    side, 23, 11, screen)


class Knight(Character):

    def __init__(self, x, y, side, screen):
        super(Knight, self).__init__('Knight', x, y, 175, 156, 189, 165, 70, 4, 6, 4.5, 100,
                                     'knights/_PNG/3_KNIGHT/_WALK/_WALK_',
                                     'knights/_PNG/3_KNIGHT/_ATTACK/_ATTACK_',
                                     side, 6, 6, screen)
