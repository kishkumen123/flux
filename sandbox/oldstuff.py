
    #        if event.type == MOUSEBUTTONDOWN:
    #            if event.button == 1:
    #                Controller.m1 = True
    #            if event.button == 3:
    #                Controller.m3 = True
    #            if _globals.selection is not None:
    #                if event.button == 5 and Controller.alt:
    #                    if _globals.selection.layer > 0:
    #                        _globals.selection.layer -= 1
    #                    else:
    #                        _globals.selection.group -= 1
    #                        _globals.selection.layer = 9
    #                    for child_id in _globals.selection.children:
    #                        child = EM.get(child_id)
    #                        if child.layer > 0:
    #                            child.layer -= 1
    #                            if child.text is not None:
    #                                child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
    #                                child.text_surface = _globals.font.render(child.text, True, child.text_color)
    #                        else:
    #                            child = EM.get(child_id)
    #                            child.group -= 1
    #                            child.layer = 9
    #                            if child.text is not None:
    #                                child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
    #                                child.text_surface = _globals.font.render(child.text, True, child.text_color)

    #        if event.type == MOUSEBUTTONUP:
    #            if event.button == 1:
    #                Controller.m1 = False
    #            if event.button == 3:
    #                Controller.m3 = False
    #            if _globals.selection is not None:
    #                if event.button == 4 and Controller.alt:
    #                    if _globals.selection.layer < 9:
    #                        _globals.selection.layer += 1
    #                    else:
    #                        _globals.selection.group += 1
    #                        _globals.selection.layer = 0
    #                    for child_id in _globals.selection.children:
    #                        child = EM.get(child_id)
    #                        if child.layer < 9:
    #                            child.layer += 1
    #                            if child.text is not None:
    #                                child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
    #                                child.text_surface = _globals.font.render(child.text, True, child.text_color)
    #                        else:
    #                            child = EM.get(child_id)
    #                            child.group += 1
    #                            child.layer = 0
    #                            if child.text is not None:
    #                                child.text = str(child._id) + ":G-%s:L-%s" % (child.group, child.layer)
    #                                child.text_surface = _globals.font.render(child.text, True, child.text_color)

