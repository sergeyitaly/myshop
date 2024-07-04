import clsx from 'clsx'
import { FormikInput } from '../../UI/FormikInput/FormikInput'
import { Form, Formik} from 'formik'
import { FormikCheckBox } from '../../UI/FormikCheckBox/FormikCheckBox'
import { FormikTextArea } from '../../UI/FormikTextArea/FormikTextArea'
import { useState } from 'react'
import { OrderFormBox } from '../../../pages/Order/OrderFormBox/OrderFormBox'
import { MainButton } from '../../UI/MainButton/MainButton'
import { OrderInfo } from '../../OrderInfo/OrderInfo'
import { CheckBoxComment } from '../../CheckBoxComment/CheckBoxComment'
import styles from './OrderForm.module.scss'
import { OrderFormModel } from './order-form.model'
import { ProductAndPriceFormikUpdate } from './ProductAndPriceFormikUpdate/ProductAndPriceFormikUpdate'


const initialValues: OrderFormModel = {
    firstName: '',
    lastName: '',
    email: '',
    phone: '',
    comment: '',
    isAnotherRecipient: false,
    isPresent: false,
    products: [],
    totalPrice: 0
}

interface OrderFormProps {
    className?: string
}


export const OrderForm = ({
    className
}: OrderFormProps) => {

    const [isOpenComment, setOpenComment] = useState<boolean>(false)

    const handleClickAddComment = () => {
        setOpenComment(!isOpenComment)
    }

    return (
            <Formik
                initialValues={initialValues}
                onSubmit={(form) => {
                    console.log(form);
                    
                }}
            >
                <Form className={clsx(styles.form, className)}>
                    <OrderFormBox
                        title='Отримувач'
                    >
                        <div className={styles.inputsContainer}>
                            <FormikInput label="Ім'я" name='firstName'/>
                            <FormikInput label="Прізвище" name='lastName'/>
                            <FormikInput label="Телефон" name='phone'/>
                            <FormikInput label="Email" name='email'/>
                            <div className={clsx(styles.anotherPersonBox) }>
                                <FormikCheckBox 
                                    name='isAnotherRecipient' 
                                />
                                 <CheckBoxComment 
                                    text='Отримувач - інша особа'
                                />
                                <button 
                                    className={styles.commentButton}
                                    onClick={handleClickAddComment}
                                >{!isOpenComment ? 'Додати коментар' : 'Прибрати коментар'}</button>
                                {
                                    isOpenComment &&
                                    <FormikTextArea 
                                        className={styles.textArea}
                                        name='comment'
                                        placeholder='Тут можна написати коментар'
                                    />
                                }
                            </div>
                        </div>
                    </OrderFormBox>

                    <OrderFormBox
                        title='Доставка'
                    >
                        <OrderInfo text='Самовивіз з магазину'/>
                    </OrderFormBox>
                    
                    <OrderFormBox
                        title='Оплата'
                    >
                        <OrderInfo text='Оплата при отриманні'/>
                    </OrderFormBox>
                   
                    <OrderFormBox
                        title='Додатково'
                    >
                        <div className={styles.presentBox}>
                            <FormikCheckBox 
                                name='isPresent' 
                            />
                            <CheckBoxComment 
                                text='Запакувати як подарунок'
                            />
                        </div>
                    </OrderFormBox>
                    <MainButton
                        title='Оформити замовлення'
                        color='black'
                    />
                    <ProductAndPriceFormikUpdate/>
                </Form>
            </Formik>
    )
}