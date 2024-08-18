class SignedIntConverter:
    # url에 들어가는 수가 음수도 가능하도록 (floor 설정)
    regex = '-?\d+'

    def to_python(self, value):
        return int(value)

    def to_url(self, value):
        return str(value)
