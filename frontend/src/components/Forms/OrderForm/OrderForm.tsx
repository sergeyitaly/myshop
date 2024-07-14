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
import { useBasket } from '../../../hooks/useBasket'
import { EmptyItemsErrorHandler } from '../EmptyItemsErrorHandler'


const initialValues: OrderDTO = {
  name: '',
  surname: '',
  email: '',
  phone: '+380',
  receiver: false,
  present: false,
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

    const {clearBasket} = useBasket()

    const [createOrder, {isSuccess, error, isError, isLoading}] = useCreateOrderMutation()

    let errorResponce: CreateOrderErrorResponce | null = null
    if(isError){
        errorResponce = error as CreateOrderErrorResponce
    }

    useEffect (() => {

        if(isSuccess){
            navigate(ROUTE.THANK)
            clearBasket()
        }

    }, [isSuccess, clearBasket, navigate])
    

    const handleClickAddComment = () => {
        setOpenComment(!isOpenComment)
    }

    return (
        
            <Formik
                initialValues={initialValues}
                validationSchema={orderValidSchema}
                onSubmit={(form) => {
                    createOrder(form)
                }}
            >
                
                <Form className={clsx(styles.form, className)}>
                    <OrderFormBox
                        title='Отримувач'
                    >
                        <button type='button'
                            onClick={() => {
                                clearBasket()
                            }}
                        >Button</button>
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
                                    type='button'
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
                                <EmptyItemsErrorHandler name='order_items'/>
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
                                name='present' 
                            />
                            <CheckBoxComment 
                                text='Запакувати як подарунок'
                            />
                        </div>
                    </OrderFormBox>
                    <MainButton
                        title={isLoading ? 'Завантажую...' : 'Оформити замовлення'}
                        color='black'
                        disabled={isLoading}
                    />
                    <ProductAndPriceFormikUpdate/>
                    <ServerErrorHandling
                        errors={errorResponce && errorResponce.data}
                    />
                </Form>
            </Formik>
    )
}