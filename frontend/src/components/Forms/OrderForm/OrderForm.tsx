import clsx from 'clsx'
import { FormikInput } from '../../UI/FormikInput/FormikInput'
import { Form, Formik} from 'formik'
import { FormikCheckBox } from '../../UI/FormikCheckBox/FormikCheckBox'
import { FormikTextArea } from '../../UI/FormikTextArea/FormikTextArea'
import { useEffect, useState } from 'react'
import { OrderFormBox } from '../../../pages/Order/OrderFormBox/OrderFormBox'
import { MainButton } from '../../UI/MainButton/MainButton'
import { OrderInfo } from '../../OrderInfo/OrderInfo'
import { CheckBoxComment } from '../../CheckBoxComment/CheckBoxComment'
import styles from './OrderForm.module.scss'
import { ProductAndPriceFormikUpdate } from './ProductAndPriceFormikUpdate/ProductAndPriceFormikUpdate'
import { OrderDTO } from '../../../models/dto'
import { CreateOrderErrorResponce, useCreateOrderMutation } from '../../../api/orderSlice'
import { orderValidSchema } from './validationSchema'
import { ServerErrorHandling } from './ServerErrorHandling'
import { useNavigate } from 'react-router-dom'
import { ROUTE } from '../../../constants'
import { AppInput } from '../../UI/AppInput/AppInput'


const initialValues: OrderDTO = {
  name: '',
  surname: '',
  email: '',
  phone: '',
  receiver: false,
  order_items: [],
  receiver_comments: ''
}

interface OrderFormProps {
    className?: string
}


export const OrderForm = ({
    className
}: OrderFormProps) => {

    const navigate = useNavigate()

    const [isOpenComment, setOpenComment] = useState<boolean>(false)

    const [createOrder, {isSuccess, error, isError}] = useCreateOrderMutation()

    let errorResponce: CreateOrderErrorResponce | null = null
    if(isError){
        errorResponce = error as CreateOrderErrorResponce
    }

    useEffect (() => {

        isSuccess &&
        navigate(ROUTE.THANK)

    }, [isSuccess])
    

    const handleClickAddComment = () => {
        setOpenComment(!isOpenComment)
    }

    return (
            <Formik
                initialValues={initialValues}
                validationSchema={orderValidSchema}

                onSubmit={(form) => {
                    console.log(form);
                    createOrder(form)
                }}
            >
                <Form className={clsx(styles.form, className)}>
                    <OrderFormBox
                        title='Отримувач'
                    >
                        <div className={styles.inputsContainer}>
                            <FormikInput label="Ім'я" name='name'/>
                            <FormikInput label="Прізвище" name='surname'/>
                            <FormikInput label="Телефон" name='phone'/>
                            <FormikInput label="Email" name='email'/>
                            <div className={clsx(styles.anotherPersonBox) }>
                                <FormikCheckBox 
                                    name='receiver' 
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
                                        name='receiver_comments'
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
                    <ServerErrorHandling
                        errors={errorResponce && errorResponce.data}
                    />
                </Form>
            </Formik>
    )
}