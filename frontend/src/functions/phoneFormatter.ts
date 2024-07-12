

export function formatPhoneNumber(phoneNumber: string) {
    const regEx = new RegExp(' ', 'g')
    let phoneWithoutPlus = ''
    let fullNumber = ''

    let hasPlus = phoneNumber[0] === '+'

    if(hasPlus) {
        phoneWithoutPlus = phoneNumber.replace(regEx, '').slice(1)
    }
    else {
        phoneWithoutPlus = phoneNumber.replace(regEx, '').slice(0)
    }

    const lastSimbol = (phoneNumber[phoneNumber.length-1]);

    if(isNaN(+lastSimbol)){
        phoneWithoutPlus = phoneWithoutPlus.slice(0, -1)
    }


    if(phoneNumber){
        let countryCode = phoneWithoutPlus.slice(0,2)
        let operatorCode = phoneWithoutPlus.slice(2,5)
        let number1 = phoneWithoutPlus.slice(5,8)
        let number2 = phoneWithoutPlus.slice(8,10)
        let number3 = phoneWithoutPlus.slice(10,12)
        fullNumber = `+${countryCode} ${operatorCode} ${number1} ${number2} ${number3}`
    }

    return {
        phone: fullNumber.replace(regEx, ''), 
        formatedPhone: fullNumber.trim()
    }
  }