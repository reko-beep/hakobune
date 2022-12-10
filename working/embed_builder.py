from discord.ui import View, Select, button, Modal, select, Button, TextInput
from discord import SelectOption , Message, Interaction, Embed, ButtonStyle, TextStyle, File
from discord.ext.commands import Context
import asyncio
import json
from text_to_image import Parser

class EmbedView(View):

    def __init__(self, ctx: Context, message: Message, embed_data_list : list = [], selected_embed : int = 0, selected_field: int = 0):

        super().__init__(timeout=180)
        self.embed_data_list = embed_data_list
        self.selected_embed_idx = selected_embed
        self.message = message
        self.ctx = ctx
        self.parser = Parser()



        if len(self.embed_data_list) == 0:
            self.embed_data_list.append(self.create_embed())
            self.selected_embed_idx = 0

        self.field_dropdown = FieldDropdown(self, 1, selected_field)
        self.add_item(self.field_dropdown)

       

    
    def create_embed(self, title: str='Main Title', description: str='Write description here', url : str='https://cdn-icons-png.flaticon.com/512/1548/1548784.png', 
                    color: int =16777215, footer_icon: str='https://cdn-icons-png.flaticon.com/512/1548/1548784.png', 
                    footer_text: str='footer text here', thumb: str = 'https://cdn-icons-png.flaticon.com/512/1548/1548784.png', image: str = 'https://cdn-icons-png.flaticon.com/512/1548/1548784.png',
                    author_name: str = 'author name here', author_url : str = 'https://cdn-icons-png.flaticon.com/512/1548/1548784.png', author_icon : str = 'https://cdn-icons-png.flaticon.com/512/1548/1548784.png',
                    fields  = [{'name': 'field one', 'value': 'value here', 'inline': False}]):
        return {
            "title": title,
            "description": description, 
            "url": url,
            "color": color,
            "footer": {
            "icon_url": footer_icon,
            "text": footer_text
            },
            "thumbnail": {
            "url": thumb
            },
            "image": {
            "url": image
            },
            "author": {
            "name": author_name,
            "url": author_url,
            "icon_url": author_icon
            },
            "fields": fields
        }

    def create_build_embed(self):
        return {
    "footer": {
        "text": "Character Name Here"
    },
    "thumbnail": {
        "url": "https://i.imgur.com/47mFsx4.png"
    },
    "fields": [
        {
            "inline": "true",
            "name": "Best Weapon(s):",
            "value": "weapons name here"
        },
        {
            "inline": "true",
            "name": "Replacement Weapon:",
            "value": "weapons name here"
        },
        {
            "inline": "false",
            "name": "Best Artifact Set:",
            "value": "artifacts name here"
        },
        {
            "inline": "false",
            "name": "Second Best Artifact Set:",
            "value": "artifacts name here"
        },
        {
            "inline": "false",
            "name": "Third Best Artifact Set:",
            "value": "artifacts name here"
        },
        {
            "inline": "true",
            "name": "Main Stats Priority",
            "value": "artifact piece (goblet, sand) : stat"
        },
        {
            "inline": "true",
            "name": "Substats Priority",
            "value": "stats here"
        },
        {
            "inline": "false",
            "name": "Talent Priority",
            "value": "**1)** Talent Type : Talent Name\n**2)** Talent Type : Talent Name\n**3)** Talent Type : Talent Name\n"
        },
        {
            "inline": "false",
            "name": "Notes:",
            "value": "Normal Attack talent does not have to be raised at all for this build. "
        }
    ],
    "color": 10147839,
    "type": "rich",
    "title": "Character name | Build Type here"
}

    def create_field(self, name: str = 'field title', value: str = 'field value', inline : bool = False):

        return {'name': name, 'value' : value, 'inline': inline}
    
    async def page(self, change_index: int):

        if change_index == +1:
            if self.selected_embed_idx < len(self.embed_data_list):
                self.selected_embed_idx += change_index
                await self.update_view()
        
        if change_index == -1:
            if self.selected_embed_idx > 0:
                self.selected_embed_idx += change_index
                await self.update_view()

    def __parse_image(self, value: str):

        if not value.startswith('http'):
            parsed = self.parser.find_image(value)
            if parsed != value:
                return parsed
            else:
                return 'https://i.imgur.com/3vNbB8O.jpg'
        return value

    async def update_view(self, selected_field : int = 0):
        print('selected index', self.selected_embed_idx)

        '''
        parse images here
        '''

        
        await self.set_property(None, 'thumbnail', self.__parse_image(self.get_property('thumbnail', True, 'url')), 'nothing', True, 'url', False)
        await self.set_property(None, 'image', self.__parse_image(self.get_property('image', True, 'url')), 'nothing', True, 'url', False)
        await self.set_property(None, 'author', self.__parse_image(self.get_property('icon_url', True, 'url')), 'nothing', True, 'icon_url', False)

        embed = Embed.from_dict(self.embed_data_list[self.selected_embed_idx])
        print(self.embed_data_list[self.selected_embed_idx])
        await self.message.edit(content=f'Embeds ({self.selected_embed_idx+1}|{len(self.embed_data_list)})',embed=embed,view=EmbedView(self.ctx, self.message, self.embed_data_list, self.selected_embed_idx, selected_field))
    

    async def set_property(self, interaction: Interaction, property_name: str, property_value: str, message: str, sub_dict: bool= False, sub_property: str = '', ephemeral_=True):
        if property_value == 'Not yet setup':
            property_value = ''
        if property_name not in self.embed_data_list[self.selected_embed_idx]:
            self.embed_data_list[self.selected_embed_idx][property_name] = ''
        if property_name in self.embed_data_list[self.selected_embed_idx]:
            if sub_dict:
                if type(self.embed_data_list[self.selected_embed_idx][property_name]) != dict:
                    self.embed_data_list[self.selected_embed_idx][property_name] = dict()
                self.embed_data_list[self.selected_embed_idx][property_name][sub_property] = property_value
            else:
                if property_value.isdigit():
                    self.embed_data_list[self.selected_embed_idx][property_name] = int(property_value) 
                else:
                    self.embed_data_list[self.selected_embed_idx][property_name] = property_value        
        if ephemeral_:
            await self.edit_ephemeral(interaction, message)
      


    async def edit_ephemeral(self, interaction : Interaction, content: str):

        if interaction.response.is_done():

            await interaction.edit_original_response(content=content)
        
        else:
             
            await interaction.response.send_message(content=content, ephemeral=True)
    
    def get_property(self, property_name: str, sub_dict: bool=False, sub_property: str = ''):

        if property_name in self.embed_data_list[self.selected_embed_idx]:           
            if sub_dict:             
                if sub_property in self.embed_data_list[self.selected_embed_idx][property_name]:
                    return self.embed_data_list[self.selected_embed_idx][property_name][sub_property]
            else:
                return self.embed_data_list[self.selected_embed_idx][property_name]
        return 'Not yet setup'

    @button(label='←', style=ButtonStyle.blurple)
    async def previous(self,interaction: Interaction, button:Button):
        if interaction.user == self.ctx.author:
            await self.page(-1)
            await self.edit_ephemeral(interaction, 'previous embed selected!')

    @button(label='→', style=ButtonStyle.blurple)
    async def next(self, interaction: Interaction, button: Button):
        if interaction.user == self.ctx.author:
            await self.page(+1)
            await self.edit_ephemeral(interaction, 'next embed selected!')

    @button(label='Create embed', style=ButtonStyle.green, emoji='📦')
    async def new(self, interaction : Interaction, button:Button):
        if interaction.user == self.ctx.author:
            new = self.create_build_embed()
            self.embed_data_list.append(new)
            self.selected_embed_idx = len(self.embed_data_list)-1

            await self.update_view()
            await self.edit_ephemeral(interaction, 'new embed created and selected!')
    
    @button(label='Author', style=ButtonStyle.green, emoji='🎗️')
    async def author(self,interaction : Interaction, button:Button):
        if interaction.user == self.ctx.author:
            await interaction.response.send_modal(AuthorFields(self, 'Editing author fields'))
            await self.edit_ephemeral(interaction, 'new embed created and selected!')

    @button(label='Base', style=ButtonStyle.green, emoji='🧱')
    async def base(self, interaction : Interaction, button:Button):
        if interaction.user == self.ctx.author:
            await interaction.response.send_modal(BaseFields(self, 'Editing base fields'))
            await self.edit_ephemeral(interaction, 'base fields updated!')

    @button(label='Images', style=ButtonStyle.green, emoji='🖼️')
    async def images(self, interaction : Interaction, button:Button):
        if interaction.user == self.ctx.author:
            await interaction.response.send_modal(ImageFields(self, 'Editing image fields'))
            await self.edit_ephemeral(interaction, 'image fields updated!')

    @button(label='Footer', style=ButtonStyle.green, emoji='📝')
    async def footer(self,interaction : Interaction, button:Button):
        if interaction.user == self.ctx.author:
            await interaction.response.send_modal(FooterFields(self, 'Editing footer fields'))
            await self.edit_ephemeral(interaction, 'footer fields updated!')

    @button(label='Remove field', style=ButtonStyle.green, emoji='❌')
    async def remove_field(self,interaction : Interaction, button:Button):
        if interaction.user == self.ctx.author:
            field_index = self.field_dropdown.selected_field
            field = self.embed_data_list[self.selected_embed_idx]['fields'][field_index]

            self.embed_data_list[self.selected_embed_idx]['fields'].pop(field_index)

            await self.update_view()
            await self.edit_ephemeral(interaction, f"removed field {field['name']}!")

    @button(label='Add field', style=ButtonStyle.green, emoji='➕')
    async def add_field(self,interaction : Interaction, button:Button):
        if interaction.user == self.ctx.author:            
            field = self.create_field()           

            self.embed_data_list[self.selected_embed_idx]['fields'].append(field)
            await self.update_view()
            await self.edit_ephemeral(interaction, f"added field {field['name']}!")

    @button(label='Save', style=ButtonStyle.primary, emoji='➕')
    async def save(self, interaction: Interaction, button: Button):
        if interaction.user == self.ctx.author:
            with open("embed.json", 'w') as f:
                json.dump(self.embed_data_list, f, indent=1)
            
            await self.ctx.send(file=File('embed.json', filename='embed.json'))
        
        await self.edit_ephemeral(interaction, f"saved to embed.json and sent")
                
class FieldDropdown(Select):
    


    def __init__(self, view : EmbedView, page: int, selected_field: int = 0) -> None:

        super().__init__(min_values=1, max_values=1)
        self.page = page
        self.field_index = 0
        self.view_ = view
        self.selected_field = selected_field
        print(self.view_.embed_data_list[self.view_.selected_embed_idx])
        if len(self.view_.embed_data_list[self.view_.selected_embed_idx]['fields']) == 0:
            self.placeholder = 'Select a field!'
        else:
            self.placeholder = self.view_.embed_data_list[self.view_.selected_embed_idx]['fields'][selected_field]['name']

        if len(self.view_.embed_data_list[self.view_.selected_embed_idx]['fields']) != 0:
            self.populate_fields()
        else:            
            self.options += [SelectOption(label='No fields added yet!', value='none')]
    
    def populate_fields(self):

        maxoptions = 21
        options_to_add = self.view_.embed_data_list[self.view_.selected_embed_idx]['fields']
        pages = 0
        if len(options_to_add) == 0:
            pages = len(options_to_add) // maxoptions
        if pages == 0:
            pages += 1

        if self.page < pages:
            self.options.append(SelectOption(label='Next'))
        if self.page > 1:
            self.options.append(SelectOption(label='Previous'))
        for page in list(range(1, pages + 1, 1)):
            max_index = len(options_to_add) if 21*page > len(options_to_add) else 21*page
            self.options += [SelectOption(label=opt['name'], value=options_to_add.index(opt)) for opt in options_to_add[21 *(page-1): max_index]]

    async def callback(self, interaction: Interaction):  
        if interaction.user == self.view_.ctx.author:
            if self.values[0] != 'none':
                if int(self.values[0]) <= len(self.view_.embed_data_list[self.view_.selected_embed_idx]['fields']):
                    self.field_index = int(self.values[0])
                    self.selected_field = self.field_index
                    data_ = self.view_.embed_data_list[self.view.selected_embed_idx]['fields'][self.field_index]
                    self.placeholder = data_['name']
                    await interaction.response.send_modal(Fields( self.view_, self.field_index, data_['name']))
                    await self.view_.edit_ephemeral(interaction=interaction,content=f'Editing {self.values[0]} field')






       


class BaseFields(Modal):
    def __init__(self, view: EmbedView, title: str) -> None:
        super().__init__(title=title, timeout=180)

        self.view = view
        #
        # base fields
        #


        self.title_field = TextInput(label='Title',default=self.view.get_property('title'),placeholder=self.view.get_property('title'), style=TextStyle.long, max_length=256, required=True)
        self.title_url = TextInput(label='Url',default=self.view.get_property('url'),placeholder=self.view.get_property('url'), style=TextStyle.long, required=False)
        self.description = TextInput(label='Description',default=self.view.get_property('description'), placeholder=self.view.get_property('description'), style=TextStyle.paragraph, max_length=4000, required=True)
        self.color = TextInput(label='Hex color code',default=self.view.get_property('color'), placeholder=self.view.get_property('color'), style=TextStyle.short, max_length=15, required=True)

        fields = (self.title_field, self.title_url, self.description, self.color)
        for field in fields:
            self.add_item(field)

    async def on_submit(self, interaction: Interaction, /) -> None:
        await self.view.set_property(interaction, 'title', self.title_field.value, 'base fields set')
        await self.view.set_property(interaction, 'url', self.title_url.value, 'base fields set')      
        await self.view.set_property(interaction, 'color', self.color.value, 'base fields set')
        await self.view.set_property(interaction, 'description', self.description.value, 'base fields set')

        await self.view.update_view()

        return await super().on_submit(interaction)

class AuthorFields(Modal):
    def __init__(self, view: EmbedView, title: str) -> None:
        super().__init__(title=title, timeout=180)

        self.view = view
        #
        # base fields
        #


        self.author_field = TextInput(label='Author name',default=self.view.get_property('author', True, 'name'),placeholder=self.view.get_property('author', True, 'name'), style=TextStyle.long, required=True)
        self.author_icon_url = TextInput(label='Author icon url',default=self.view.get_property('author', True, 'icon_url'),placeholder=self.view.get_property('author', True, 'icon_url'), style=TextStyle.long, required=False)
        self.author_url = TextInput(label='Author url',default=self.view.get_property('author', True, 'url'),placeholder=self.view.get_property('author', True, 'url'), style=TextStyle.long, max_length=1000, required=False)

        fields = (self.author_field, self.author_url, self.author_icon_url)
        for field in fields:
            self.add_item(field)

    async def on_submit(self, interaction: Interaction, /) -> None:

        await self.view.set_property(interaction, 'author', self.author_field.value, 'author values set', True, 'name')
        await self.view.set_property(interaction, 'author', self.author_icon_url.value, 'author values set', True, 'icon_url')
        await self.view.set_property(interaction, 'author', self.author_url.value, 'author values set', True, 'url')
        await self.view.update_view()

        return await super().on_submit(interaction)


class FooterFields(Modal):
    def __init__(self, view: EmbedView, title: str) -> None:
        super().__init__(title=title, timeout=180)

        self.view = view
        #
        # base fields
        #


        self.footer_field = TextInput(label='Footer text',default=self.view.get_property('footer', True, 'text'),placeholder=self.view.get_property('footer', True, 'text'), style=TextStyle.paragraph, required=True)
        self.footer_icon_url = TextInput(label='Footer icon url',default=self.view.get_property('footer', True, 'icon_url'),placeholder=self.view.get_property('footer', True, 'icon_url'), style=TextStyle.long, required=False)
     

        fields = (self.footer_field, self.footer_icon_url)
        for field in fields:
            self.add_item(field)

    async def on_submit(self, interaction: Interaction, /) -> None:
        
        await self.view.set_property(interaction, 'footer', self.footer_field.value, 'footer values set', True, 'text')
        await self.view.set_property(interaction, 'footer', self.footer_icon_url.value, 'footer values set', True, 'icon_url')
        await self.view.update_view()

        return await super().on_submit(interaction)

class ImageFields(Modal):
    def __init__(self, view: EmbedView, title: str) -> None:
        super().__init__(title=title, timeout=180)

        self.view = view
        #
        # base fields
        #


        self.image_url = TextInput(label='Image url',default=self.view.get_property('image', True, 'url'),placeholder=self.view.get_property('image', True, 'url'), style=TextStyle.paragraph, required=True)
        self.thumbnail_url = TextInput(label='Author icon url',default=self.view.get_property('thumbnail', True, 'url'),placeholder=self.view.get_property('thumbnail', True, 'url'), style=TextStyle.long, required=False)
        

        fields = (self.image_url, self.thumbnail_url)
        for field in fields:
            self.add_item(field)

    async def on_submit(self, interaction: Interaction, /) -> None:
        await self.view.set_property(interaction, 'image', self.image_url.value, 'image values set', True, 'url')
        await self.view.set_property(interaction, 'thumbnail', self.thumbnail_url.value, 'imagevalues set', True, 'url')

        await self.view.update_view()

        return await super().on_submit(interaction)


class Fields(Modal):
    def __init__(self, view: EmbedView, field_index: int, title: str) -> None:
        super().__init__(title=title, timeout=180)

        self.view = view
        #
        # base fields
        #

        self.field_index = field_index
        name = self.view.embed_data_list[self.view.selected_embed_idx]['fields'][self.field_index]['name']        
        value = self.view.embed_data_list[self.view.selected_embed_idx]['fields'][self.field_index]['value']
        self.field_title = TextInput(label='Field name',default=name, placeholder=name, style=TextStyle.long, required=True)
        self.field_value = TextInput(label='Field value',default=value, placeholder=value, style=TextStyle.paragraph, required=True)
     

        fields = (self.field_title, self.field_value)
        for field in fields:
            self.add_item(field)

    async def on_submit(self, interaction: Interaction, /) -> None:
        self.view.embed_data_list[self.view.selected_embed_idx]['fields'][self.field_index]['name'] = self.field_title.value
        self.view.embed_data_list[self.view.selected_embed_idx]['fields'][self.field_index]['value'] = self.field_value.value

        await self.view.update_view(self.field_index)
        await self.view.edit_ephemeral(interaction, 'field edited!')
        