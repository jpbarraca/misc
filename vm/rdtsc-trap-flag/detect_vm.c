/*
    Simple VM Detection based on rdtsc exception handling
    RDTSC with TF will issue exception, but behaviour is distinct in a VM
*/

#include <stdio.h>
#define __USE_GNU
#include <ucontext.h>
#include <signal.h>
#include <unistd.h>
#include <stdlib.h>

// Generate a SIGTRAP using TF and RDTSC
int detect_vm(){
    asm(" \
        pushf; \
        or dword ptr[rsp], 0x100; \
        popf; \
        rdtsc; \
        nop;\
        nop; \
    ");
}

// Running in a bare host will yeld one exception at detect_vm+15
// Running inside a VM will yeld one or more exceptions at addressed higher than detect_vm+15
void trap_handler(int sig, siginfo_t* code, void *arg) {
    ucontext_t *context = (ucontext_t *)arg;
    if(((long long int) context->uc_mcontext.gregs[REG_RIP] - ((long long int) detect_vm)) != 15) {
        printf("VM Detected\n");
        exit(0);
    }
}

void main() {
    // Setup the SIGTRAP exception handler
    struct sigaction action_handler;
    action_handler.sa_sigaction = trap_handler;
    action_handler.sa_flags = SA_SIGINFO;
    sigaction(SIGTRAP, &action_handler,NULL);
 
    //Detect the VM
    detect_vm();

    //Do stuff
    sleep(1) ; 
    while(1) {
        printf("normal program execution. No VM\n");
        sleep(1);
    }
}
