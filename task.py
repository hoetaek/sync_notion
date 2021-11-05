from tododist_task import create_label, get_all_labels


class Task:
    def __init__(self, id, title, label_ids: list, end_date):
        self.id = id
        self.title = title
        self.labels = label_ids
        self.end_date = end_date

    @classmethod
    def from_todoist(cls, todoist_obj):
        id = todoist_obj["id"]
        title = todoist_obj["content"]
        end_date = todoist_obj.get("due").get("datetime") if todoist_obj.get("due") != None else None
        return cls(id, title, end_date)

    @classmethod
    def from_gtd(cls, gtd):
        id = gtd.todoist_id
        title = gtd.title
        labels = gtd.reminder
        end_date = gtd.date
        return cls(id, title, labels, end_date)

    def check_and_create_labels(labels):
        todoist_all_labels = [todoist_label["name"] for todoist_label in get_all_labels()]
        labels_not_in_todoist = [label for label in labels if label not in todoist_all_labels]
        for label in labels_not_in_todoist:
            create_label(label)

    def commit():
        


