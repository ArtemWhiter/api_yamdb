

###тестовые модели, чтобы только запускалось

class Title(models.Model):
    
    def __str__(self):
        return self.title


class Comment(models.Model):

    def __str__(self):
        return self.title


class Post(models.Model):

    def __str__(self):
        return self.title


class Categorie(models.Model):

    def __str__(self):
        return self.title


class Genre(models.Model):
    
    def __str__(self):
        return self.title