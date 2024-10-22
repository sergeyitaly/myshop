interface FeedbackCard {
    id: number
    firstQuestion: string
    secondQuestion?: string
    ratingButtons: boolean
}

export const cards: FeedbackCard[]= [
    {
        id: 1,
        firstQuestion: 'Оцініть дизайн сайту!',
        secondQuestion: 'Що вам найбільше сподобалось в сайті?',
        ratingButtons: true
    },
    {
        id: 2,
        firstQuestion: 'Оцініть навігацію сайту( чи зручно і легко користуватись).',
        secondQuestion: 'Що вам найбільше сподобалось в сайті?',
        ratingButtons: true
    },
    {
        id: 8,
        firstQuestion: 'Оцініть швидкість завантаження сайту!',
        secondQuestion: 'Чого на вашу думку не вистачає в сайті?',
        ratingButtons: true
    },
    {
        id: 4,
        firstQuestion: 'Чи вважаєте що інформації на сайті достатньо? Якщо ні, то чого саме не вистачає?',
        ratingButtons: true
    },
    {
        id: 5,
        firstQuestion: 'Чи помітили ви якісь помилки на сайті?',
        ratingButtons: true
    },
    {
        id: 6,
        firstQuestion: 'Які зміни ви б порадили для покращення сайту?',
        ratingButtons: false
    },
    {
        id: 7,
        firstQuestion: 'Якщо у вас виникли додаткові запитання або коментарі можете записати їх тут.',
        ratingButtons: false
    },

]