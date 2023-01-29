# export const slugify = (str: string): string => {
#   const join = "-";
#   return str
#     .toLowerCase()
#     .replace(/[^a-z0-9-]+/g, join)
#     .replace(/-+/g, join)
#     .split(join)
#     .filter(Boolean)
#     .join(join);
# };

import re


def slugify(value: str) -> str:
    join_char = "-"

    value = value.lower()
    value = re.sub(r"[^a-z0-9-]+", join_char, value)
    value = re.sub(r"-+", join_char, value)

    return value
