import { useEffect, useState } from "react";
import { useNavigate } from "react-router-dom";
import clsx from "clsx";
import { FormikInput } from "../../UI/FormikInput/FormikInput";
import { Form, Formik } from "formik";
import { FormikCheckBox } from "../../UI/FormikCheckBox/FormikCheckBox";
import { FormikTextArea } from "../../UI/FormikTextArea/FormikTextArea";
import { OrderFormBox } from "../../../pages/Order/OrderFormBox/OrderFormBox";
import { MainButton } from "../../UI/MainButton/MainButton";
import { OrderInfo } from "../../OrderInfo/OrderInfo";
import { CheckBoxComment } from "../../CheckBoxComment/CheckBoxComment";
import { OrderDTO } from "../../../models/dto";
import {
    CreateOrderErrorResponce,
    useCreateOrderMutation,
} from "../../../api/orderSlice";
import { getOrderValidSchema } from "./validationSchema";
import { ServerErrorHandling } from "./ServerErrorHandling";
import { ROUTE } from "../../../constants";
import { useBasket } from "../../../hooks/useBasket";
import { EmptyItemsErrorHandler } from "../EmptyItemsErrorHandler";
import { ProductAndPriceFormikUpdate } from "./ProductAndPriceFormikUpdate/ProductAndPriceFormikUpdate";
import { useTranslation } from "react-i18next";
import bird from "./bird.svg";
import styles from "./OrderForm.module.scss";
import { STORAGE } from "../../../constants";

interface OrderFormProps {
    className?: string;
}

export const OrderForm = ({ className }: OrderFormProps) => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    const [isOpenComment, setOpenComment] = useState<boolean>(false);
    const [isOpenCongrats, setOpenCongrats] = useState<boolean>(false);
    const { clearBasket } = useBasket();
    const [createOrder, { isSuccess, error, isError, isLoading }] =
        useCreateOrderMutation();

    const [language, setLanguage] = useState<string>(
        localStorage.getItem(STORAGE.LANGUAGE) || "uk"
    );

    useEffect(() => {
        // Update language in localStorage when it changes
        if (language) {
            localStorage.setItem(STORAGE.LANGUAGE, language);
        }
    }, [language]);

    useEffect(() => {
        const storedLanguage = localStorage.getItem(STORAGE.LANGUAGE) || "uk";
        setLanguage(storedLanguage);
    }, []);

    const initialValues: OrderDTO = {
        name: "",
        surname: "",
        email: "",
        phone: "+380",
        receiver: false,
        present: false,
        order_items: [],
        receiver_comments: "",
        congrats: "",
        language: language,
    };

    let errorResponce: CreateOrderErrorResponce | null = null;
    if (isError) {
        errorResponce = error as CreateOrderErrorResponce;
    }

    useEffect(() => {
        if (isSuccess) {
            navigate(ROUTE.THANK);
            clearBasket();
        }
    }, [isSuccess]);

    const handleClickAddComment = () => {
        setOpenComment(!isOpenComment);
    };

    const handleClickAddCongrats = () => {
        setOpenCongrats(!isOpenCongrats);
    };

    return (
        <Formik
            initialValues={{
                ...initialValues,
            }}
            validationSchema={getOrderValidSchema(t)}
            onSubmit={(form) => {
                createOrder(form);
            }}
        >
            <Form className={clsx(styles.form, className)}>
                <OrderFormBox title={t("recipient")}>
                    <div className={styles.inputsContainer}>
                        <FormikInput label={t("first_name")} name="name" />
                        <FormikInput label={t("last_name")} name="surname" />
                        <FormikInput label={t("phone")} name="phone" />
                        <FormikInput label={t("email")} name="email" />

                        <div className={clsx(styles.anotherPersonBox)}>
                            <FormikCheckBox name="receiver" />
                            <CheckBoxComment
                                text={t("receiver_checkbox_label")}
                            />
                            <button
                                className={styles.commentButton}
                                type="button"
                                onClick={handleClickAddComment}
                            >
                                {!isOpenComment
                                    ? t("add_comment")
                                    : t("remove_comment")}
                            </button>
                            {isOpenComment && (
                                <FormikTextArea
                                    className={styles.textArea}
                                    name="receiver_comments"
                                    placeholder={t("comment_placeholder")}
                                />
                            )}
                            <EmptyItemsErrorHandler name="order_items" />
                        </div>
                    </div>
                </OrderFormBox>

                <OrderFormBox title={t("pickup_store")}>
                    <OrderInfo text={t("pickup_store")} />
                </OrderFormBox>

                <OrderFormBox title={t("payment_on_delivery")}>
                    <OrderInfo text={t("payment_on_delivery")} />
                </OrderFormBox>

                <OrderFormBox title={t("additionaly")}>
                    <div className={styles.giftWrapper}>
                        <div className={styles.giftCheckbox}>
                            <FormikCheckBox name="present" />
                            <CheckBoxComment text={t("wrap_as_gift")} />
                        </div>

                        <div className={styles.giftContainer}>
                            <p className={styles.giftTitle}>
                                <img src={bird} alt={t("gift_title")} />{" "}
                                {t("gift_title")}
                            </p>
                            <button
                                type="button"
                                className={styles.giftButton}
                                onClick={handleClickAddCongrats}
                            >
                                <span>
                                    {!isOpenCongrats
                                        ? t("add_congrats")
                                        : t("remove_congrats")}
                                </span>
                            </button>

                            {isOpenCongrats && (
                                <FormikTextArea
                                    className={styles.giftTextArea}
                                    name="congrats"
                                    placeholder={t("gift_message")}
                                />
                            )}
                        </div>
                    </div>
                </OrderFormBox>

                <MainButton
                    title={isLoading ? t("loading") : t("place_order")}
                    color="black"
                    disabled={isLoading}
                />
                <ServerErrorHandling
                    errors={errorResponce && errorResponce.data}
                />
                <ProductAndPriceFormikUpdate />
            </Form>
        </Formik>
    );
};
