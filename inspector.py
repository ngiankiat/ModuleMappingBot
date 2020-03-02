class Inspect:
    def __init__(self, df, uni, module_list):
        print("I'm at inspect function!")
        self.df = df
        self.uni = uni
        self.module_list = module_list

    def run(self):
        x = self.inspect()
        return x

    def inspect(self):
        result = []
        filtered_rows = tuple(filter(lambda x: self.uni in x[3], self.df))

        for x in self.module_list:
            for y in filtered_rows:
                if x in y[1]:
                    result += [y]

        reply_text = ("\n\n####### For " + filtered_rows[0][3] + " #######")
        for z in result:
            reply_text += "\n\n" + z[1] + " can be mapped to " + z[2]
        reply_text += "\n\n##################################################"

        return reply_text  # we return a result