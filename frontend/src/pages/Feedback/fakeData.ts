interface FeedbackCard {
    firstQuestion: string
    secondQuestion?: string
    value: null | number
}

export const cards: FeedbackCard[]= [
    {
        firstQuestion: 'Оцініть дизайн сайту!',
        secondQuestion: 'Що вам найбільше сподобалось в сайті?',
        value: 0
    },
    {
        firstQuestion: 'Оцініть навігацію сайту( чи зручно і легко користуватись).',
        secondQuestion: 'Що вам найбільше сподобалось в сайті?',
        value: 0
    },
    {
        firstQuestion: 'Оцініть швидкість завантаження сайту!',
        secondQuestion: 'Чого на вашу думку не вистачає в сайті?',
        value: 0
    },
    {
        firstQuestion: 'Чи вважаєте що інформації на сайті достатньо? Якщо ні, то чого саме не вистачає?',
        value: 0
    },
    {
        firstQuestion: 'Чи помітили ви якісь помилки на сайті?',
        value: 0
    },
    {
        firstQuestion: 'Які зміни ви б порадили для покращення сайту?',
        value: null
    },
    {
        firstQuestion: 'Якщо у вас виникли додаткові запитання або коментарі можете записати їх тут.',
        value: null
    },

]