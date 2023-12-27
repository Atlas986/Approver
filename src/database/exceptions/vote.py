class AlreadyVoted(Exception):

    def __str__(self):
        return f'Current user is already voted to the poll'
