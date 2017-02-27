from django.db import models

class House(models.Model):

    owner = models.OneToOneField(
        'players.Player', 
        null = True, 
        blank = True, 
        on_delete = models.SET_NULL,
        related_name = 'house_owner'
    )
    
    name = models.CharField(
        max_length = 50,
        unique = True
    )
    
    paid = models.PositiveIntegerField(
        default = 0
    )
    
    warnings = models.PositiveSmallIntegerField(
        default = 0
    )
    
    last_warning = models.DateTimeField(
        default = None,
        null = True,
        blank = True
    )

    class Meta:
        db_table = 'houses'

    def __str__(self):
        return self.name

    @property
    def get_owner_name(self):
        return self.owner.name if self.owner else 'nobody'

class HouseList(models.Model):
    
    house = models.ForeignKey(
        'houses.House', 
        on_delete = models.CASCADE
    )
    
    list_id = models.IntegerField(
        default = 0
    )
    
    list = models.TextField(
        max_length = 1000,
        default = '',
        blank = True
    )

    class Meta:
        db_table = 'house_lists'
        unique_together = ['house', 'list_id']

class HouseTile(models.Model):
    
    house = models.ForeignKey(
        'houses.House', 
        on_delete = models.CASCADE
    )
    
    x = models.PositiveIntegerField()
    y = models.PositiveIntegerField()
    z = models.PositiveSmallIntegerField()

    class Meta:
        db_table = 'house_tiles'
        index_together = ['x', 'y', 'z']

class HouseTileItem(models.Model):
    
    tile = models.ForeignKey(
        'houses.HouseTile', 
        on_delete = models.CASCADE
    )
    
    s_id = models.IntegerField(db_index = True)
    p_id = models.IntegerField(default = 0)
    item_type = models.IntegerField()
    count = models.IntegerField(default = 0)
    attributes = models.BinaryField(default = b'')

    class Meta:
        db_table = 'house_tileitems'
        unique_together = ['tile', 's_id']


