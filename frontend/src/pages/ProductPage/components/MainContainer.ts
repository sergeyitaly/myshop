import styled from '@emotion/styled'

export const MainContainer = styled.div<{isLoading: boolean}>`
    position: relative;
    display: flex;
    flex-direction: column;
    gap: clamp(50px, 10vw, 155px);
    transition: .8s;
    filter: ${({isLoading}) => (
        isLoading ? 'blur(5px)' : 'none'
    )} 
`
