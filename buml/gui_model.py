####################
# STRUCTURAL MODEL #
####################

from besser.BUML.metamodel.structural import (
    Class, Property, Method, Parameter,
    BinaryAssociation, Generalization, DomainModel,
    Enumeration, EnumerationLiteral, Multiplicity,
    StringType, IntegerType, FloatType, BooleanType,
    TimeType, DateType, DateTimeType, TimeDeltaType,
    AnyType, Constraint, AssociationClass, Metadata, MethodImplementationType
)

# Enumerations
Genre: Enumeration = Enumeration(
    name="Genre",
    literals={
            EnumerationLiteral(name="Poetry"),
			EnumerationLiteral(name="Thriller"),
			EnumerationLiteral(name="History"),
			EnumerationLiteral(name="Technology"),
			EnumerationLiteral(name="Romance"),
			EnumerationLiteral(name="Horror"),
			EnumerationLiteral(name="Adventure"),
			EnumerationLiteral(name="Philosophy"),
			EnumerationLiteral(name="Cookbooks"),
			EnumerationLiteral(name="Fantasy")
    }
)

# Classes
Book = Class(name="Book")
Library = Class(name="Library")
Author = Class(name="Author")

# Book class attributes and methods
Book_title: Property = Property(name="title", type=StringType)
Book_pages: Property = Property(name="pages", type=IntegerType)
Book_stock: Property = Property(name="stock", type=IntegerType)
Book_price: Property = Property(name="price", type=FloatType)
Book_release: Property = Property(name="release", type=DateType)
Book_genre: Property = Property(name="genre", type=Genre)
Book_m_decrease_stock: Method = Method(name="decrease_stock", parameters={Parameter(name='qty', type=IntegerType)}, implementation_type=MethodImplementationType.CODE)
Book_m_decrease_stock.code = """def decrease_stock(self, qty: int):
    \"\"\"
    Decrease the available stock by the given quantity.

    :param qty: Number of items to remove from stock
    :raises ValueError: If qty is negative or exceeds available stock
    \"\"\"
    if qty <= 0:
        raise ValueError("Quantity must be a positive integer")

    if qty > self.stock:
        raise ValueError(
            f"Cannot decrease stock by {qty}. Only {self.stock} items available."
        )

    self.stock -= qty

"""
Book.attributes={Book_genre, Book_pages, Book_price, Book_release, Book_stock, Book_title}
Book.methods={Book_m_decrease_stock}

# Library class attributes and methods
Library_name: Property = Property(name="name", type=StringType)
Library_web_page: Property = Property(name="web_page", type=StringType)
Library_address: Property = Property(name="address", type=StringType)
Library_telephone: Property = Property(name="telephone", type=StringType)
Library_m_cheapest_book_by: Method = Method(name="cheapest_book_by", parameters={Parameter(name='author', type=Author)}, type=StringType, implementation_type=MethodImplementationType.BAL)
Library_m_cheapest_book_by.code = """def cheapest_book_by(author:Author) -> str {
    cheapest:Book = null;
	price = 1000000000.0;
	for(book in this.books){
        if(book.authors.contains(author)
			&& book.price <= price){
            cheapest = book;
			price = book.price;
		}
    }
	return cheapest.title;
}"""
Library.attributes={Library_address, Library_name, Library_telephone, Library_web_page}
Library.methods={Library_m_cheapest_book_by}

# Author class attributes and methods
Author_name: Property = Property(name="name", type=StringType)
Author_birth: Property = Property(name="birth", type=DateType)
Author.attributes={Author_birth, Author_name}

# Relationships
books: BinaryAssociation = BinaryAssociation(
    name="books",
    ends={
        Property(name="library", type=Library, multiplicity=Multiplicity(1, 9999)),
        Property(name="books", type=Book, multiplicity=Multiplicity(0, 9999))
    }
)
books_1: BinaryAssociation = BinaryAssociation(
    name="books_1",
    ends={
        Property(name="authors", type=Author, multiplicity=Multiplicity(1, 9999)),
        Property(name="books", type=Book, multiplicity=Multiplicity(0, 9999))
    }
)


# OCL Constraints
constraint_Book_0_1: Constraint = Constraint(
    name="constraint_Book_0_1",
    context=Book,
    expression="context Book inv inv1: self.pages> 10",
    language="OCL"
)

# Domain Model
domain_model = DomainModel(
    name="Library",
    types={Book, Library, Author, Genre},
    associations={books, books_1},
    constraints={constraint_Book_0_1},
    generalizations={},
    metadata=None
)


###############
#  GUI MODEL  #
###############

from besser.BUML.metamodel.gui import (
    GUIModel, Module, Screen,
    ViewComponent, ViewContainer,
    Button, ButtonType, ButtonActionType,
    Text, Image, Link, InputField, InputFieldType,
    Form, Menu, MenuItem, DataList,
    DataSource, DataSourceElement, EmbeddedContent,
    Styling, Size, Position, Color, Layout, LayoutType,
    UnitSize, PositionType, Alignment
)
from besser.BUML.metamodel.gui.dashboard import (
    LineChart, BarChart, PieChart, RadarChart, RadialBarChart, Table, AgentComponent,
    Column, FieldColumn, LookupColumn, ExpressionColumn, MetricCard, Series
)
from besser.BUML.metamodel.gui.events_actions import (
    Event, EventType, Transition, Create, Read, Update, Delete, Parameter
)
from besser.BUML.metamodel.gui.binding import DataBinding

# Module: GUI_Module

# Screen: wrapper
wrapper = Screen(name="wrapper", description="Book", view_elements=set(), is_main_page=True, route_path="/book", screen_size="Medium")
wrapper.component_id = "page-book-0"
i2u8k = Text(
    name="i2u8k",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="i2u8k",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "i2u8k"}
)
iof5a = Link(
    name="iof5a",
    description="Link element",
    label="Book",
    url="/book",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="iof5a",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/book", "id": "iof5a"}
)
i660i = Link(
    name="i660i",
    description="Link element",
    label="Library",
    url="/library",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i660i",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/library", "id": "i660i"}
)
ifuv2 = Link(
    name="ifuv2",
    description="Link element",
    label="Author",
    url="/author",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ifuv2",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/author", "id": "ifuv2"}
)
ie6vj = ViewContainer(
    name="ie6vj",
    description=" component",
    view_elements={iof5a, i660i, ifuv2},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="ie6vj",
    display_order=1,
    custom_attributes={"id": "ie6vj"}
)
ie6vj_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
ie6vj.layout = ie6vj_layout
i1mon = Text(
    name="i1mon",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="i1mon",
    display_order=2,
    custom_attributes={"id": "i1mon"}
)
i6214 = ViewContainer(
    name="i6214",
    description="nav container",
    view_elements={i2u8k, ie6vj, i1mon},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="i6214",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "i6214"}
)
i6214_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
i6214.layout = i6214_layout
ifo9y = Text(
    name="ifo9y",
    content="Book",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="ifo9y",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "ifo9y"}
)
ipk1q = Text(
    name="ipk1q",
    content="Manage Book data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="ipk1q",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "ipk1q"}
)
table_book_0_col_0 = FieldColumn(label="Title", field=Book_title)
table_book_0_col_1 = FieldColumn(label="Pages", field=Book_pages)
table_book_0_col_2 = FieldColumn(label="Stock", field=Book_stock)
table_book_0_col_3 = FieldColumn(label="Price", field=Book_price)
table_book_0_col_4 = FieldColumn(label="Release", field=Book_release)
table_book_0_col_5 = FieldColumn(label="Genre", field=Book_genre)
table_book_0_col_6_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "library")
table_book_0_col_6 = LookupColumn(label="Library", path=table_book_0_col_6_path, field=Library_name)
table_book_0_col_7_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "authors")
table_book_0_col_7 = LookupColumn(label="Authors", path=table_book_0_col_7_path, field=Author_name)
table_book_0 = Table(
    name="table_book_0",
    title="Book List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_book_0_col_0, table_book_0_col_1, table_book_0_col_2, table_book_0_col_3, table_book_0_col_4, table_book_0_col_5, table_book_0_col_6, table_book_0_col_7],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-book-0",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "Book List", "data-source": "class_oho5ergc3_mjikkmod", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'title', 'label': 'Title', 'columnType': 'field', '_expanded': False}, {'field': 'pages', 'label': 'Pages', 'columnType': 'field', '_expanded': False}, {'field': 'stock', 'label': 'Stock', 'columnType': 'field', '_expanded': False}, {'field': 'price', 'label': 'Price', 'columnType': 'field', '_expanded': False}, {'field': 'release', 'label': 'Release', 'columnType': 'field', '_expanded': False}, {'field': 'genre', 'label': 'Genre', 'columnType': 'field', '_expanded': False}, {'field': 'library', 'label': 'Library', 'columnType': 'lookup', 'lookupEntity': 'class_06blhjj3h_mjikkmod', 'lookupField': 'name', '_expanded': False}, {'field': 'authors', 'label': 'Authors', 'columnType': 'lookup', 'lookupEntity': 'class_d3f0di6lb_mjikkmoe', 'lookupField': 'name', '_expanded': False}], "id": "table-book-0", "filter": ""}
)
domain_model_ref = globals().get('domain_model') or next((v for k, v in globals().items() if k.startswith('domain_model') and hasattr(v, 'get_class_by_name')), None)
table_book_0_binding_domain = None
if domain_model_ref is not None:
    table_book_0_binding_domain = domain_model_ref.get_class_by_name("Book")
if table_book_0_binding_domain:
    table_book_0_binding = DataBinding(domain_concept=table_book_0_binding_domain, name="BookDataBinding")
else:
    # Domain class 'Book' not resolved; data binding skipped.
    table_book_0_binding = None
if table_book_0_binding:
    table_book_0.data_binding = table_book_0_binding
i9ez4 = Button(
    name="i9ez4",
    description="Button component",
    label="+ decrease_stock",
    buttonType=ButtonType.CustomizableButton,
    actionType=ButtonActionType.RunMethod,
    method_btn=Book_m_decrease_stock,
    instance_source="table-book-0",
    is_instance_method=True,
    styling=Styling(size=Size(padding="6px 14px", font_size="13px", font_weight="600", text_decoration="none", letter_spacing="0.01em"), position=Position(display="inline-flex", cursor="pointer", transition="background 0.2s"), color=Color(background_color="linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", text_color="#fff", color_palette="default", border_radius="4px", border="none", box_shadow="0 1px 4px rgba(37,99,235,0.10)"), layout=Layout(layout_type=LayoutType.FLEX, align_items="center")),
    component_id="i9ez4",
    tag_name="button",
    display_order=0,
    css_classes=["action-button-component"],
    custom_attributes={"type": "button", "data-button-label": "+ decrease_stock", "data-action-type": "run-method", "data-method": "method_rb01uirsh_mjikkmod", "data-instance-source": "table-book-0", "id": "i9ez4", "method-class": "Book", "endpoint": "/book/{book_id}/methods/decrease_stock/", "is-instance-method": "true", "input-parameters": {'qty': {'type': 'int', 'required': True}}, "instance-source": "table-book-0"}
)
i63lj = ViewContainer(
    name="i63lj",
    description=" component",
    view_elements={i9ez4},
    styling=Styling(size=Size(margin_top="20px"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_wrap="wrap", gap="10px")),
    component_id="i63lj",
    display_order=3,
    custom_attributes={"id": "i63lj"}
)
i63lj_layout = Layout(layout_type=LayoutType.FLEX, flex_wrap="wrap", gap="10px")
i63lj.layout = i63lj_layout
iglfg = ViewContainer(
    name="iglfg",
    description="main container",
    view_elements={ifo9y, ipk1q, table_book_0, i63lj},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="iglfg",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "iglfg"}
)
iglfg_layout = Layout(flex="1")
iglfg.layout = iglfg_layout
id3fo = ViewContainer(
    name="id3fo",
    description=" component",
    view_elements={i6214, iglfg},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="id3fo",
    display_order=0,
    custom_attributes={"id": "id3fo"}
)
id3fo_layout = Layout(layout_type=LayoutType.FLEX)
id3fo.layout = id3fo_layout
wrapper.view_elements = {id3fo}


# Screen: wrapper_2
wrapper_2 = Screen(name="wrapper_2", description="Library", view_elements=set(), route_path="/library", screen_size="Medium")
wrapper_2.component_id = "page-library-1"
iivo5 = Text(
    name="iivo5",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="iivo5",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "iivo5"}
)
ie88s = Link(
    name="ie88s",
    description="Link element",
    label="Book",
    url="/book",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ie88s",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/book", "id": "ie88s"}
)
izf8r = Link(
    name="izf8r",
    description="Link element",
    label="Library",
    url="/library",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="izf8r",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/library", "id": "izf8r"}
)
i657y = Link(
    name="i657y",
    description="Link element",
    label="Author",
    url="/author",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i657y",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/author", "id": "i657y"}
)
ilxjr = ViewContainer(
    name="ilxjr",
    description=" component",
    view_elements={ie88s, izf8r, i657y},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="ilxjr",
    display_order=1,
    custom_attributes={"id": "ilxjr"}
)
ilxjr_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
ilxjr.layout = ilxjr_layout
ic4aj = Text(
    name="ic4aj",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="ic4aj",
    display_order=2,
    custom_attributes={"id": "ic4aj"}
)
ip8me = ViewContainer(
    name="ip8me",
    description="nav container",
    view_elements={iivo5, ilxjr, ic4aj},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="ip8me",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "ip8me"}
)
ip8me_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
ip8me.layout = ip8me_layout
if48p = Text(
    name="if48p",
    content="Library",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="if48p",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "if48p"}
)
iqtsl = Text(
    name="iqtsl",
    content="Manage Library data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="iqtsl",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "iqtsl"}
)
table_library_1_col_0 = FieldColumn(label="Name", field=Library_name)
table_library_1_col_1 = FieldColumn(label="Web Page", field=Library_web_page)
table_library_1_col_2 = FieldColumn(label="Address", field=Library_address)
table_library_1_col_3 = FieldColumn(label="Telephone", field=Library_telephone)
table_library_1_col_4_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "books")
table_library_1_col_4 = LookupColumn(label="Books", path=table_library_1_col_4_path, field=Book_title)
table_library_1 = Table(
    name="table_library_1",
    title="Library List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_library_1_col_0, table_library_1_col_1, table_library_1_col_2, table_library_1_col_3, table_library_1_col_4],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-library-1",
    display_order=2,
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "Library List", "data-source": "class_06blhjj3h_mjikkmod", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'name', 'label': 'Name', 'columnType': 'field', '_expanded': False}, {'field': 'web_page', 'label': 'Web Page', 'columnType': 'field', '_expanded': False}, {'field': 'address', 'label': 'Address', 'columnType': 'field', '_expanded': False}, {'field': 'telephone', 'label': 'Telephone', 'columnType': 'field', '_expanded': False}, {'field': 'books', 'label': 'Books', 'columnType': 'lookup', 'lookupEntity': 'class_oho5ergc3_mjikkmod', 'lookupField': 'title', '_expanded': False}], "id": "table-library-1", "filter": ""}
)
domain_model_ref = globals().get('domain_model') or next((v for k, v in globals().items() if k.startswith('domain_model') and hasattr(v, 'get_class_by_name')), None)
table_library_1_binding_domain = None
if domain_model_ref is not None:
    table_library_1_binding_domain = domain_model_ref.get_class_by_name("Library")
if table_library_1_binding_domain:
    table_library_1_binding = DataBinding(domain_concept=table_library_1_binding_domain, name="LibraryDataBinding")
else:
    # Domain class 'Library' not resolved; data binding skipped.
    table_library_1_binding = None
if table_library_1_binding:
    table_library_1.data_binding = table_library_1_binding
iuseu = Button(
    name="iuseu",
    description="Button component",
    label="+ cheapest_book_by",
    buttonType=ButtonType.CustomizableButton,
    actionType=ButtonActionType.RunMethod,
    method_btn=Library_m_cheapest_book_by,
    instance_source="table-library-1",
    is_instance_method=True,
    styling=Styling(size=Size(padding="6px 14px", font_size="13px", font_weight="600", text_decoration="none", letter_spacing="0.01em"), position=Position(display="inline-flex", cursor="pointer", transition="background 0.2s"), color=Color(background_color="linear-gradient(90deg, #2563eb 0%, #1e40af 100%)", text_color="#fff", color_palette="default", border_radius="4px", border="none", box_shadow="0 1px 4px rgba(37,99,235,0.10)"), layout=Layout(layout_type=LayoutType.FLEX, align_items="center")),
    component_id="iuseu",
    tag_name="button",
    display_order=0,
    css_classes=["action-button-component"],
    custom_attributes={"type": "button", "data-button-label": "+ cheapest_book_by", "data-action-type": "run-method", "data-method": "35ef5329-889b-40f0-89ce-9836936fd8a9", "data-instance-source": "table-library-1", "id": "iuseu", "method-class": "Library", "endpoint": "/library/{library_id}/methods/cheapest_book_by/", "is-instance-method": "true", "input-parameters": {'author': {'type': 'Author', 'required': True, 'input_kind': 'lookup', 'entity': 'Author', 'lookup_field': 'name'}}, "instance-source": "table-library-1"}
)
iqlul = ViewContainer(
    name="iqlul",
    description=" component",
    view_elements={iuseu},
    styling=Styling(size=Size(margin_top="20px"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_wrap="wrap", gap="10px")),
    component_id="iqlul",
    display_order=3,
    custom_attributes={"id": "iqlul"}
)
iqlul_layout = Layout(layout_type=LayoutType.FLEX, flex_wrap="wrap", gap="10px")
iqlul.layout = iqlul_layout
i3u2r = ViewContainer(
    name="i3u2r",
    description="main container",
    view_elements={if48p, iqtsl, table_library_1, iqlul},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="i3u2r",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "i3u2r"}
)
i3u2r_layout = Layout(flex="1")
i3u2r.layout = i3u2r_layout
i98a1 = ViewContainer(
    name="i98a1",
    description=" component",
    view_elements={ip8me, i3u2r},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="i98a1",
    display_order=0,
    custom_attributes={"id": "i98a1"}
)
i98a1_layout = Layout(layout_type=LayoutType.FLEX)
i98a1.layout = i98a1_layout
wrapper_2.view_elements = {i98a1}


# Screen: wrapper_3
wrapper_3 = Screen(name="wrapper_3", description="Author", view_elements=set(), route_path="/author", screen_size="Medium")
wrapper_3.component_id = "page-author-2"
ik0iu = Text(
    name="ik0iu",
    content="BESSER",
    description="Text element",
    styling=Styling(size=Size(font_size="24px", font_weight="bold", margin_top="0", margin_bottom="30px"), color=Color(color_palette="default")),
    component_id="ik0iu",
    tag_name="h2",
    display_order=0,
    custom_attributes={"id": "ik0iu"}
)
i4gzx = Link(
    name="i4gzx",
    description="Link element",
    label="Book",
    url="/book",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="i4gzx",
    tag_name="a",
    display_order=0,
    custom_attributes={"href": "/book", "id": "i4gzx"}
)
izy8i = Link(
    name="izy8i",
    description="Link element",
    label="Library",
    url="/library",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="transparent", text_color="white", color_palette="default", border_radius="4px")),
    component_id="izy8i",
    tag_name="a",
    display_order=1,
    custom_attributes={"href": "/library", "id": "izy8i"}
)
ittq5 = Link(
    name="ittq5",
    description="Link element",
    label="Author",
    url="/author",
    styling=Styling(size=Size(padding="10px 15px", text_decoration="none", margin_bottom="5px"), position=Position(display="block"), color=Color(background_color="rgba(255,255,255,0.2)", text_color="white", color_palette="default", border_radius="4px")),
    component_id="ittq5",
    tag_name="a",
    display_order=2,
    custom_attributes={"href": "/author", "id": "ittq5"}
)
ikpoe = ViewContainer(
    name="ikpoe",
    description=" component",
    view_elements={i4gzx, izy8i, ittq5},
    styling=Styling(position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")),
    component_id="ikpoe",
    display_order=1,
    custom_attributes={"id": "ikpoe"}
)
ikpoe_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column", flex="1")
ikpoe.layout = ikpoe_layout
iucti = Text(
    name="iucti",
    content="© 2026 BESSER. All rights reserved.",
    description="Text element",
    styling=Styling(size=Size(font_size="11px", padding_top="20px", margin_top="auto"), position=Position(alignment=Alignment.CENTER), color=Color(opacity="0.8", color_palette="default", border_top="1px solid rgba(255,255,255,0.2)")),
    component_id="iucti",
    display_order=2,
    custom_attributes={"id": "iucti"}
)
iqmu7 = ViewContainer(
    name="iqmu7",
    description="nav container",
    view_elements={ik0iu, ikpoe, iucti},
    styling=Styling(size=Size(width="250px", padding="20px", unit_size=UnitSize.PIXELS), position=Position(display="flex", overflow_y="auto"), color=Color(background_color="linear-gradient(135deg, #4b3c82 0%, #5a3d91 100%)", text_color="white", color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX, flex_direction="column")),
    component_id="iqmu7",
    tag_name="nav",
    display_order=0,
    custom_attributes={"id": "iqmu7"}
)
iqmu7_layout = Layout(layout_type=LayoutType.FLEX, flex_direction="column")
iqmu7.layout = iqmu7_layout
iilbk = Text(
    name="iilbk",
    content="Author",
    description="Text element",
    styling=Styling(size=Size(font_size="32px", margin_top="0", margin_bottom="10px"), color=Color(text_color="#333", color_palette="default")),
    component_id="iilbk",
    tag_name="h1",
    display_order=0,
    custom_attributes={"id": "iilbk"}
)
iiyzy = Text(
    name="iiyzy",
    content="Manage Author data",
    description="Text element",
    styling=Styling(size=Size(margin_bottom="30px"), color=Color(text_color="#666", color_palette="default")),
    component_id="iiyzy",
    tag_name="p",
    display_order=1,
    custom_attributes={"id": "iiyzy"}
)
table_author_2_col_0 = FieldColumn(label="Name", field=Author_name)
table_author_2_col_1 = FieldColumn(label="Birth", field=Author_birth)
table_author_2_col_2_path = next(end for assoc in domain_model.associations for end in assoc.ends if end.name == "books")
table_author_2_col_2 = LookupColumn(label="Books", path=table_author_2_col_2_path, field=Book_title)
table_author_2 = Table(
    name="table_author_2",
    title="Author List",
    primary_color="#2c3e50",
    show_header=True,
    striped_rows=False,
    show_pagination=True,
    rows_per_page=5,
    action_buttons=True,
    columns=[table_author_2_col_0, table_author_2_col_1, table_author_2_col_2],
    styling=Styling(size=Size(width="100%", min_height="400px", unit_size=UnitSize.PERCENTAGE), color=Color(color_palette="default", primary_color="#2c3e50")),
    component_id="table-author-2",
    display_order=2,
    css_classes=["has-data-binding"],
    custom_attributes={"chart-color": "#2c3e50", "chart-title": "Author List", "data-source": "class_d3f0di6lb_mjikkmoe", "show-header": "true", "striped-rows": "false", "show-pagination": "true", "rows-per-page": "5", "action-buttons": "true", "columns": [{'field': 'name', 'label': 'Name', 'columnType': 'field', '_expanded': False}, {'field': 'birth', 'label': 'Birth', 'columnType': 'field', '_expanded': False}, {'field': 'books', 'label': 'Books', 'columnType': 'lookup', 'lookupEntity': 'class_oho5ergc3_mjikkmod', 'lookupField': 'title', '_expanded': False}], "id": "table-author-2", "filter": ""}
)
domain_model_ref = globals().get('domain_model') or next((v for k, v in globals().items() if k.startswith('domain_model') and hasattr(v, 'get_class_by_name')), None)
table_author_2_binding_domain = None
if domain_model_ref is not None:
    table_author_2_binding_domain = domain_model_ref.get_class_by_name("Author")
if table_author_2_binding_domain:
    table_author_2_binding = DataBinding(domain_concept=table_author_2_binding_domain, name="AuthorDataBinding")
else:
    # Domain class 'Author' not resolved; data binding skipped.
    table_author_2_binding = None
if table_author_2_binding:
    table_author_2.data_binding = table_author_2_binding
i5y9h = ViewContainer(
    name="i5y9h",
    description="main container",
    view_elements={iilbk, iiyzy, table_author_2},
    styling=Styling(size=Size(padding="40px"), position=Position(overflow_y="auto"), color=Color(background_color="#f5f5f5", color_palette="default"), layout=Layout(flex="1")),
    component_id="i5y9h",
    tag_name="main",
    display_order=1,
    custom_attributes={"id": "i5y9h"}
)
i5y9h_layout = Layout(flex="1")
i5y9h.layout = i5y9h_layout
iizs3 = ViewContainer(
    name="iizs3",
    description=" component",
    view_elements={iqmu7, i5y9h},
    styling=Styling(size=Size(height="100vh", font_family="Arial, sans-serif"), position=Position(display="flex"), color=Color(color_palette="default"), layout=Layout(layout_type=LayoutType.FLEX)),
    component_id="iizs3",
    display_order=0,
    custom_attributes={"id": "iizs3"}
)
iizs3_layout = Layout(layout_type=LayoutType.FLEX)
iizs3.layout = iizs3_layout
wrapper_3.view_elements = {iizs3}

gui_module = Module(
    name="GUI_Module",
    screens={wrapper, wrapper_2, wrapper_3}
)

# GUI Model
gui_model = GUIModel(
    name="GUI",
    package="",
    versionCode="1.0",
    versionName="1.0",
    modules={gui_module},
    description="GUI"
)
