#pragma once

#ifndef TEST_H
#define TEST_H

#if defined(DEBUG) || defined(DEBUG_BUILD)

    /**
     * If the condition is false panics and prints debug information. Built in
     * assert is not used because it does not crash well on windows and sometimes
     * the output is not visible (even in the debugger).
     */
    #define assert(cond) SAFE_MACRO({ \
        if (!(cond)) { \
            panic("Assert failed: %s", (#cond)); \
        } \
    })

#else

    #define assert(cond) ;

#endif

#endif /* TEST_H */
