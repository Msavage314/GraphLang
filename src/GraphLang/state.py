class DesmosState:
    """Manages the desmos graph state"""

    def __init__(self):
        self.expressions = []
        self.next_id = 1
        self.current_folder = None

    def add_expression(self, latex: str, color: str = "#c74440", **kwargs):
        expr = {
            "type": "expression",
            "id": str(self.next_id),
            "color": color,
            "latex": latex,
            **kwargs,
        }
        self.expressions.append(expr)
        self.next_id += 1
        return expr

    def add_folder(self, title: str):
        """Add a folder to organize expressions"""
        folder = {
            "type": "folder",
            "id": str(self.next_id),
            "title": title,
            "collapsed": False,
        }
        self.expressions.append(folder)
        self.current_folder = str(self.next_id)
        self.next_id += 1
        return folder

    def to_json(self) -> dict:
        """Convert to Desmos JSON format"""
        return {
            "version": 11,
            "randomSeed": "8c1582f5f1cdb65271c65f53058c2fc6",
            "graph": {
                "viewport": {
                    "xmin": -10,
                    "ymin": -14.286819239443817,
                    "xmax": 10,
                    "ymax": 14.286819239443817,
                }
            },
            "expressions": {"list": self.expressions},
        }
