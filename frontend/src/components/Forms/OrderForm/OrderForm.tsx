import clsx from 'clsx'
import { FormikInput } from '../../UI/FormikInput/FormikInput'
import { Form, Formik } from 'formik'
import { FormikCheckBox } from '../../UI/FormikCheckBox/FormikCheckBox'
import { FormikTextArea } from '../../UI/FormikTextArea/FormikTextArea'
import { useEffect, useState } from 'react'
import { OrderFormBox } from '../../../pages/Order/OrderFormBox/OrderFormBox'
import { MainButton } from '../../UI/MainButton/MainButton'
import { OrderInfo } from '../../OrderInfo/OrderInfo'
import { CheckBoxComment } from '../../CheckBoxComment/CheckBoxComment'
import styles from './OrderForm.module.scss'
import { OrderDTO } from '../../../models/dto'
import { CreateOrderErrorResponce, useCreateOrderMutation } from '../../../api/orderSlice'
import { orderValidSchema } from './validationSchema'
import { ServerErrorHandling } from './ServerErrorHandling'
import { useNavigate } from 'react-router-dom'
import { ROUTE } from '../../../constants'
import { useBasket } from '../../../hooks/useBasket'
import { EmptyItemsErrorHandler } from '../EmptyItemsErrorHandler'
import { ProductAndPriceFormikUpdate } from './ProductAndPriceFormikUpdate/ProductAndPriceFormikUpdate'
import { useTranslation } from 'react-i18next'; // Import useTranslation

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

    const { t } = useTranslation(); // Use useTranslation hook
    const navigate = useNavigate()
    const [isOpenComment, setOpenComment] = useState<boolean>(false)
    const { clearBasket } = useBasket()
    const [createOrder, { isSuccess, error, isError, isLoading }] = useCreateOrderMutation()

    let errorResponce: CreateOrderErrorResponce | null = null
    if (isError) {
        errorResponce = error as CreateOrderErrorResponce
    }

    useEffect(() => {
        if (isSuccess) {
            navigate(ROUTE.THANK)
            clearBasket()
        }
    }, [isSuccess])

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
                    title={t('recipient')}
                >
                    <div className={styles.inputsContainer}>
                        <FormikInput label={t('first_name')} name='name' />
                        <FormikInput label={t('last_name')} name='surname' />
                        <FormikInput label={t('phone')} name='phone' />
                        <FormikInput label={t('email')} name='email' />
                        <div className={clsx(styles.anotherPersonBox)}>
                            <FormikCheckBox
                                name='receiver'
                            />
                            <CheckBoxComment
                                text={t('receiver_checkbox_label')}
                            />
                            <button
                                className={styles.commentButton}
                                type='button'
                                onClick={handleClickAddComment}
                            >
                                {!isOpenComment ? t('add_comment') : t('remove_comment')}
                            </button>
                            {isOpenComment &&
                                <FormikTextArea
                                    className={styles.textArea}
                                    name='receiver_comments'
                                    placeholder={t('comment_placeholder')}
                                />
                            }
                            <EmptyItemsErrorHandler name='order_items' />
                        </div>
                    </div>
                </OrderFormBox>

                <OrderFormBox
                    title={t('pickup_store')}
                >
                    <OrderInfo text={t('pickup_store')} />
                </OrderFormBox>

                <OrderFormBox
                    title={t('payment_on_delivery')}
                >
                    <OrderInfo text={t('payment_on_delivery')} />
                </OrderFormBox>

                <OrderFormBox
                    title={t('wrap_as_gift')}
                >
                    <div className={styles.presentBox}>
                        <FormikCheckBox
                            name='present'
                        />
                        <CheckBoxComment
                            text={t('wrap_as_gift')}
                        />
                    </div>
                </OrderFormBox>
                <MainButton
                    title={isLoading ? t('loading') : t('place_order')}
                    color='black'
                    disabled={isLoading}
                />
                <ServerErrorHandling
                    errors={errorResponce && errorResponce.data}
                />
                <ProductAndPriceFormikUpdate />
            </Form>
        </Formik>
    )
}
