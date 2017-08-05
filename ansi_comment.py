import sublime, sublime_plugin

class AnsiCommentCommand(sublime_plugin.TextCommand):
    def run(self, edit):
        num_selections = 0
        for _ in self.view.sel():
            num_selections += 1
        if num_selections > 1:
            return

        selection = self.view.lines(self.view.sel()[0])

        # Check if we're uncommenting the line
        uncomment = True
        for line_region in selection:
            if line_region.empty():
                break
            line = self.view.substr(line_region)
            if not ("/* " in line and " */" in line):
                uncomment = False
                break

        if uncomment:
            # Uncomment the line
            for line_region in reversed(selection):
                if line_region.empty():
                    continue
                line = self.view.substr(line_region)
                newline = line.replace(" */", "")
                newline = newline.replace("/* ", "")
                newline = newline.replace("*\\", "*")
                newline = newline.replace("\\*", "*")
                self.view.replace(edit, line_region, newline)
        else:
            # Comment out the line
            col = -1
            cols = []
            for line_region in selection:
                offset = 0
                if line_region.empty():
                    continue
                for c in self.view.substr(line_region):
                    if not c.isspace():
                        break
                    offset += 1
                if col > offset or col == -1:
                    col = offset
                cols.append(col)
            for line_region in reversed(selection):
                if line_region.empty():
                    continue
                line = self.view.substr(line_region)
                prefix = line[0:col]
                content = line[col:]
                # newline = "/* " + line + " */"
                newcontent = content.replace("\\*", "\\\\*")
                newcontent = newcontent.replace("*\\", "*\\\\")
                newcontent = newcontent.replace("/*", "/\\*")
                newcontent = newcontent.replace("*/", "*\\/")
                newline = prefix + "/* " + newcontent + " */"
                self.view.replace(edit, line_region, newline)
