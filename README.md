![CI logo](https://codeinstitute.s3.amazonaws.com/fullstack/ci_logo_small.png)
# Code Institute, Milestone 3: hash-board

## Introduction

In response to the financial crisis of 2008, Satoshi Nakamoto released the Bitcoin whitepaper outlining the first decentralised public ledger technology to hit the world stage.
The network has stood strong to this day and inspired 1000s of projects build off of Satoshi's vision of a decentralised world. We now have a robust ecosystem of smart contract, NFT and decentralised financed platforms.
Pandora's box has been opened and there is no turning back.

One of the main benefits of cryptocurrencies is the public availability of the blockchain data. Previously corporations would protect vast silos of data in order to monetize it & increase their stranglehold on the market.
Public blockchains granted software developers to the ability to compete with much larger corporations by providing value to the user & not by monetizing siloed data.

Even though cryptocurrencies have been around for more than a decade, adoption rates are still relatively low. I believe this is due to the perceived complexity of the technology.
My goal for my Code Institute Milestone Project 3: Data Centric is to simplify the experience for the user by allowing them to view their blockchain data in a more intuitive graphical interface.

#### The Ethereum Network

#### Current Blockchain Interfaces

This cryptocurrency dashboard project will be reading transactions from the Ethereum blockchain. Ethereum is the market leader in smart contract technology with the largest community & developer base.
Etherscan is the leading blockchain API which allows you to view transactions, smart contracts, user accounts & on-chain metrics. After using Etherscan for the past 4 years, I have seen that very few improvements have been made to the UX. 
I believe this is the key to onboarding new users and taking smart contract platforms to the next level.

#### Planned Features


## Considerations

## UX


### Project Goals

My original idea was to introduce new people to the cryptocurrency ecosystem by creating a user-friendly interface to allow users to view their transactions in a more intuitive way.
This will allow users to view their blockchain transactions with more clarity & reduce some of the anxiety that new user will face when starting out in crypto.
This application doesn't just limit you to viewing your own transactions, the user will be able to search any transaction on the Ethereum chain and save it to their dashboard.
With this feature, users can track Ethereum whales & the movement of funds within important smart contracts. Many forensic accounting techniques can be preformed using this web application.

### User Goals

The target audience for this application reflects people within the age group of your average cryptocurrency user (16-35).

##### The user's goals are:

* To be provided with blockchain data in a format that is easy to navigate and understand.
* To use public blockchain data in order to track funds moving through the ecosystem.
* Prioritise specific transactions.
* Add small pieces of text to priority transactions.
* Update text related to priority transactions.

##### Hashboard satisfies these needs by:
* Creating a clean data layout with any unnecessary information removed.
* Allowing the user to search transactions from any public Ethereum address.
* Giving the user the ability to favourite priority transactions.
* The user is then able to add important text information related to that transaction.
* This information can be edited if it becomes outdated.
* Once a user is finished needing to view this transactions, their favourites list can be reset.

### Developer & Business Goals


##### Developer Goals

* Due to this project being my first Python web application, my main goal was to learn as much as possible about Python web development.
* In the future, I would like to work as smart contract developer. This project, even though it doesn't use any smart contract, is a great project to have in my portfolio.
* To provide an application which is a useful tool to the crypto community.
* The application should also keep the user coming back regularly due to the necessity of the product.

##### Business Goals

* Use the application's traffic to sell advertising.
* (Future Feature) Create a premium tier account for heavy users.

##### Tier Structure (Future Feature)

Limit the user to a set number of blockchain searches & favourited transactions. This will incentivise active users to upgrade to the premium tier.

Premium tier users will have unlimited access to search and adding favourite transactions.

### User Stories


1. As a user of this web application I want:
    * A clean and enjoyable UX, everything should be where I want it.
    * Fonts that are legible but something a bit different to the norm.
    * Little to no load times when the website first starts or has to complete a process.

2. As somebody looking to advertise on this website I would like:
    * Content that is family friendly and not provocative so our brand doesn't become tarnished.
    * Heavy user traffic in order to get our brand in front of as many eyeballs as possible.
    * Fast load times to ensure impatient users don't leave the site.


### User Stories Testing


1. This application satisfies the needs of the user by:
    * Having a clean UI, based on the princibles of material design.
    * Ensuring that all text on the website is leigible at a quick glance.
    * Being designed in an efficent manner, compressing data wherever possible.

2. Advertiser needs are satisfied by this project as:
    * The site's content is advertiser-friendly and non-controvertial.
    * The web application is designed to maintain users attention by providing value.
    * The application is efficiently designed.

### Design Choices

##### Responsive Front-End Framework

For this project, I decided to use the Materialize framework which is build on the principles of material design.
After completing the project using this new framework, I can safely say that I prefer it more then Bootstrap which I have used on my previous 2 milestone projects.
It appears to provide more feedback to the user when they are navigating throughout the web application while remaining responsive on most devices.

##### Icons

All icons for this application have been sourced from [Google Fonts](https://fonts.google.com/icons) collected from the Material Icons library. As the designer of the web application, the selection of the icons must be done in line with other successful applications. 

###### Favourite Icon

![Favourite Icon](readme-imgs/favourite_screenshot.JPG)

After searching a public Ethereum address, it's transactions will then be added to your hashboard. The next step is for the user to prioritise certain transactions which they deem important. The heart icon has been used for nearly a decade now in order to represent important items within a list.

###### Edit Icon

![Edit Icon](readme-imgs/edit_screenshot.JPG)

Once the user has added their priority transactions to their favourite's list, a text note may have been added. The edit icon is what allows the user to change the note stored in relation to their transaction. I have chosen the pen icon from Material Icons as it has been used by previous developers when interacting with text-based components. 

###### Delete Icon

![Delete Icon](readme-imgs/delete_screenshot.JPG)

Finally, once the user has no more need to prioritise a specific transaction, there needs to be a way in order for the user to be able to clean up their favourite's list. There could only be one realistic choice for this icon as it has been used so predominantly in software design. I decided to use the rubbish bin icon due to it's intuitive nature.


##### Fonts

There has only been one font chosen for this project due to the nature of the application. I wanted to keep the application as minimal as possible. Only having one font, reduces complexity in the eye of the user leading to a more streamlined experience.

###### Varela Round

![Varela Font Example](readme-imgs/font_varela.JPG)

The font chosen was taken from [Google Fonts](https://fonts.google.com/). I chose this font as it was extremely legibile & simple while still remaining fun and playful.

##### Colours

The colour palate was chosen to emulate the design choices of the Ethereum foundation. Since it's inception, Ethereum's colour theme has always been different hues of blue. 

###### Teal lighten-2

This is the specific colour chosen within the Materialize framework for the navbar as it lends itself nicely to the Ethereum colour scheme.

###### Materialize Button

The colour of the buttons throughout the site is unchanged as it is the primary button colour for the Materialize framework. During the design process, I noticed that this shade of blue complemented the teal hue of the navbar.


## Key Elements

This section will outline the key elements within this application giving descriptions on the purpose of each element.

##### Modals

Modals have been used several times throughout the application in order to confirm if a user would like to proceed with an irreversible process. This is considered best-practice in web development as the user could easily push a button by mistake and trigger a process which cannot be undone.

As the majority of the web application is simply styled in order to create that sleek minimal look, modal design is where I have allowed for some more adventurous styling. As you can see in the example above, once a modal is activated, a shadow effect is applied across the screen behind the modal. A secondary teal shadow has been added to the border of the modal to give it a 3D-like appearance.

###### Log Out Modal Example

![Log Out Modal](readme-imgs/modal_example2.JPG)

###### Sign Out Modal Example

![Sign Out Modal](readme-imgs/signout_example.JPG)

###### Reset Modal Example

![Reset Modal](readme-imgs/reset_modal.JPG)


##### Data Tables(Desktop View)

For the desktop view, a data table was used to represent the Ethereum transaction data. Data tables allow more information to be displayed to the user without causing confusion. In order to aid this property, as much of the non-critical data has been removed.

##### Gallery Slider(Mobile/Tablet View)

From the beginning of the design of the application, I knew that a separate view would be needed to display transaction information to mobile/tablet users. The data table wouldn't be able to sufficiently show all data fields to the user in a satisfying manner.

In order to counteract this, a gallery style view was created for mobile/tablet users. Each transaction is represented by a slide within a larger gallery. Users swipe from left to right in order to access different transactions. I believe this is a design which many mobile users are familiar with due to the rise of social media applications such as Instagram.


#### Error Handling

##### Flash Messages

In order to communicate information to the user, an alert system was needed. Flask has a built-in messaging library known as flash, which we can use to send important information to the frontend. Along with passing data, we can also categorise these messages into pre-defined groups such as "error" & "info". This allows us to change the styling of the HTML element displaying the alert depending on the category of the message.

[Example of successful flash message](readme-imgs/success_flash.JPG)

[Example of an error flash message](readme-imgs/error_flash.JPG)


##### API Exceptions

##### Lottie Player Animations


### User Interaction

##### Blockchain Search

##### Priority Transactions

##### Notes



## Implementation

This section will outline the technologies & processes used in the design & implementation of this application.

#### Materialize Framework

#### MongoDB

#### Etherscan API

#### Python

#### Jinja

#### Flask



### Modules

#### API Requests

#### Asyncronous Requests

#### Mongo DB Backend

#### Mongo DB Jobs

## Performance

## Testing

## Bugs Discovered

## Deployment

## Credit

[Materialize Framework Documentation](https://materializecss.com/)

[HTML Element fade-out](https://stackoverflow.com/questions/1911290/make-div-text-disappear-after-5-seconds-using-jquery#1911308)

[Etherscan API](https://etherscan.io/apis)

[Flask Documentation](https://flask.palletsprojects.com/en/1.1.x/)

[Ethereum Documentation](https://ethereum.org/en/)

[Mongo DB Documentation](https://docs.mongodb.com/)

[Python Docstrings](https://www.geeksforgeeks.org/python-docstrings/)

[Pylint Error Help](https://learn.adafruit.com/improve-your-code-with-pylint/pylint-errors)

[Heroku Documentation](https://devcenter.heroku.com/categories/python-support)

[Markdown Cheat Sheet](https://www.markdownguide.org/cheat-sheet)

[Displaying Information to the user efficiently](https://www.youtube.com/watch?v=Ox9MW9Z8srE&list=PLOPo1bGrV4htxbQCS3CPZ59O1kpPdE7PK)

[]()

[]()

[]()

[]()

[]()

[]()





## Wireframes

## Dependancies

#### Requirements.txt

#### Web3