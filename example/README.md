# Input file references

There are two main sections of the input file: `schema` and `dependencies`. Sections are denoted by the line `section:schema` or `section:dependencies` at the beginning of each section. `schema` section defines the table names, as well as column names, types, and other options for each columns. `dependencies` section defines any functional dependencies that might not have been reflected in the schema definition. Every input file must include at least the `schema` section. `dependencies` section is optional.

The input file is quite rigid, and uses space as a delimiter, so please follow the guideline closely and avoid adding spaces where it is not needed, otherwise the input might not be read correctly.

Please see file `example/input_full.txt` for a comprehensive example of how to use each and every configurable input options.

## I. Schema section

### Tables

Syntax for each table within the schema section is as follows:

```
table {table_name} amount={number} (
    {column_name} {column_type} [column_options...]
    ...
)
...
```

Example:

```
table students amount=100 (
    id id primary_key
    first_name first_name
    email email related=students.first_name
    graduation_year number range=2000..2022
    fav_colour color
)
```

Declare each new table with a line that starts with `table`, followed by `table_name`, the amount, and a pair of parentheses in which all the columns are declared. Each column declaration must be on its own line, and end with `)`

`table_name` must not have spaces.

`amount={number}` denotes how many rows of record to generate within the table. If the amount is not specified, the default is 10 rows.

### Column types and column options

`column_name` must not have spaces.

`column_type` must not have spaces, and must be of a type available below.

`column_option` must be of the format `{option-name}={option-value}`. Neither option-name nor option-value can have space. Some options allow multiple values, in that case they must be separated with commas (`,`).

List of all `[column_type]`s and all their corresponding `[column_options]`:
- `string`: a random string from the values defined.
    - `max_length={number}` maximum length the string can have.
    - `min_length={number}` minimum length the string can have.
    - `values=[values...]` provide the possible values that the string can have. Example: `semester string values=Fall,Spring,Special`. This option is required for the `string` type to generate values. If omitted, all generated values will be empty string. When generating values, underscores `_` will be converted to spaces. E.g. `values=one_thing,many_thing` will generate columns with values `"one thing"`, `"many thing"`
- `number`: a random number
    - `range={min}..{max}` specify minimum and maximum value (inclusive). `min` and `max` can be omitted e.g. `range=..999` or `range=12..`. The lower and upper bound are defaulted to 0 and 1000 respectively.
    - `decimal` or `decimal=true` use this when you need a decimal. If not specified will default to integer. Use together with `decimal_places`.
    - `decimal_places={number}` only applies when using `decimal`. Specify the exact decimal places of generated values. If omitted will default to 3 decimal places.
- `id`: represent numerical id of a row. Automatically generate self-incrementing integer as id.
    - if `reference` option is specified, or the id is part of any relationship, the column will adapt and reference the related foreign id. See further detail on how to use references below this section.
- `first_name`: random person's first name
- `last_name`: random person's last name
- `email`: random email based on person's first and last name
    - `related={first_name_column},{last_name_column}` Generate an email for a given first name and last name. In the current implementation of the program, the type `email` will only generate an email for a person, so their first name and last name column is required, and should be provided using the `related` option. Full column name with table name is required. Example: `related=students.first_name,students.last_name`.
- `date`: a random date
    - `range={start_year}..{end_year}` Generate a random date. In the current implementation of the program, can only specify a year as the start and end range. The generated date will be of the form DD/MM/YYYY that exist between the given year (inclusive).
- `time`: a random time
    - the time will be of the format HH:MM:SS

### Primary key / unique

- Use the option `primary_key` on any column when you require it to be a primary key.
    - In the current implementation of the program, composite primary key is not supported. However you can achieve the same goal (to a certain extent) by declaring functional dependencies.
- Use the option `unique` or `unique=true` on any column to have every row be unique.
    - In the current implementation of the program, the are some drawbacks on the unique constraint in some edge cases. For example if you declare a column to have a one-to-one relationship of another column, yet you ask the generator to generate only 10 entries while the other column to generate 100 entries, the one-to-one relationship will not hold.

### References

To declare table and column relationships, a.k.a. references, you can declare it as an option of a column or as standalone declarations.

You should only declare the relationship once. Avoid declaring multiple times (Eg declare many-to-one in one column and one-to-many in the other column).

#### Reference as option of a column

- `reference={relationship}{table_name}{column_name}`
    - used to specify a relationship / foreign key
    - relationship is one of:
        - `>` many to one
        - `~` one to one
        - `<` one to many
        - `<>` many to many
        - if unspecified, default to many-to-many
    - Example:
        - `instructor_id id reference=>instructors.id`: column `instructor_id` has many-to-one relationship with the `id` column of another table `instructors`.

#### Standalone reference declaration

Table column references can be declared outside of `table`:

```
reference: {table_name}.{column_name} {relationship} {table_name}.{column_name}
```

The line must start with `reference:`. Please take note that there are no space before the `:`

`relationship` must be of `>` `~` `<` or `<>` and cannot be empty.

## II. Dependencies section

You can declare functional dependencies that happens within a table, and the generator will try to adhere to the dependencies. The syntax for dependencies is as follows:

```
table {table_name} (
    {column_name} [column_name...] -> {column_name} [column_name]
    ...
)
...
```

Please see an example within the file `example/input_number_dep.txt`

It is not possible to declare functional dependencies cross-table.

The program does not support multi-valued dependencies.