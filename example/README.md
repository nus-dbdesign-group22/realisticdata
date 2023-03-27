# Input file references

There are two main sections of the input file: `schema` and `dependencies`. Sections are denoted by the line `section:schema` or `section:dependencies` at the beginning of each section. `schema` section defines the table names, as well as field names, types, and other requirements for each fields. `dependencies` section defines any functional dependencies or multi-valued dependencies that are not reflected in the schema section. Every input file must include at least the `schema` section. `dependencies` section is optional.

## I. Schema section

### Tables

Syntax for each table within the schema section is as follows:

```
table {table_name} [table_options...] (
    {field_name} {field_type} [field_options...]
    ...
)
...
```

`table_name` must not have spaces. If they have spaces, they need to be enclosed in quotes (`'like this'` or `"like this"`)

`[table_options]` can be of the following:

- `amount={number}` : generate this exact amount of rows in this table.
- `amount={min}..{max}` : generate a random amount of rows in this table, within range. `min` can be omitted, but `max` cannot. Eg: `amount=..100`.
- if `amount` is omitted, default to 10 rows.

### Field types and field options

`field_name` must not have spaces. If they have spaces, they need to be enclosed in quotes (`'like this'` or `"like this"`).

`field_option` must be of the format `{option-name}={option-value}`. Values must not have space. If values contain space they must be enclosed in quotes. Some options allow multiple values, in that case they must be separated with commas (`,`). The commas must be outside of the quotes: `option="value 1",two,"value three"`.

List of all `[field_type]`s and all their corresponding `[field_options]`:
- `string`: a random alphanumeric string
    - `max_length={number}` maximum length the string can have.
    - `min_length={number}` minimum length the string can have.
    - `values=[values...]` limits the string to only these values. Example: `semester string values="Fall","Spring","Special"`.
- `number`: a random number
    - `range={min}..{max}` specify minimum and maximum value (inclusive). `min` and `max` can be omitted e.g. `range=..999` or `range=12..`. The upper and lower bound will depend on python's built-in primitives.
    - `decimal=true` use this when you need a decimal. If not specified will default to integer. Addition option with `decimal_places`.
    - `decimal_places={number}` only applies when `decimal=true`. Specify exact decimal places. Can use `{min}..{max}` for flexible decimal places.
- `id`: represent numerical id of a row.
    - if `primary_key` option is specified, the field will be a unique self-incrementing integer.
    - if `reference` option is specified, the field will be a foreign key referencing the id of another table. See further detail for the `reference` option below.
    - if neither `primary_key` nor `reference` option is specified, the field will be a random unique integer number.
- `first_name`: random person's first name
    - inherit all of `string`'s options
- `last_name`: random person's last name
    - inherit all of `string`'s options
- `email`: random email
    - inherit all of `string`'s options
- `text`: random dummy text / paragraph
    - `max_length_words={number}` maximum words in length
    - inherit all of `string`'s options
- `date`: a random date
    - `range={start}..{end}` WIP
- `timestamp`: a random timestamp
    - WIP

### Global field options

These field options applies to ALL field types:

- `reference={relationship}{table_name}{field_name}`
    - used to specify a relationship / foreign key
    - relationship is one of:
        - `>` many to one
        - `~` one to one
        - `<` one to many
        - `<>` many to many
        - if unspecified, default to many-to-many
    - Example:
        - `instructor_id id reference=>instructors.id`: field `instructor_id` has many-to-one relationship with the `id` field of another table `instructors`.
- `unique=true` every row in the table must be unique
- `nullable` or `nullable={percentage}`: can have NULL in some rows. If `percentage` is specified, how much of the column is NULL. 0% means no NULL 100$ means all NULL. Cannot be used with `id primary_key`.
- `emptyable` or `emptyable={percentage}`: can be empty for some rows. If `percentage` is specified, how much of the column is empty. 0% means no row is empty 100$ means all row is empty. Can only be used with `string` and `string`-inherited types.

## II. Dependencies section

Syntax for each table within the dependencies section is as follows:

```
table {table_name} (
    {field_name} [field_name...] -> {field_name} [field_name]
    ...
)
...
```

