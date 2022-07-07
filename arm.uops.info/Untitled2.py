#!/usr/bin/env python
# coding: utf-8

# In[1]:


from unicorn import *
from unicorn.arm64_const import *
from keystone import *


# In[2]:


from keystone import *


# In[3]:


ks = Ks(KS_ARCH_ARM64, KS_MODE_LITTLE_ENDIAN)


# In[4]:


# memory address where emulation starts
ADDRESS = 0x1000000
mu = Uc(UC_ARCH_ARM64, UC_MODE_LITTLE_ENDIAN)
mu.mem_map(ADDRESS, 2 * 1024 * 1024)


# In[5]:


code = ks.asm("sshll v0.8H, v1.8B, 2")[0]
code = b''.join(map(lambda x: x.to_bytes(1,'big'), code))


# In[6]:


mu.mem_write(ADDRESS, code)


# In[7]:


mu.reg_write(UC_ARM64_REG_V1, (1<<128)-1)


# In[8]:


mu.emu_start(ADDRESS, ADDRESS + len(code))


# In[9]:


bin(mu.reg_read(UC_ARM64_REG_V1))


# In[10]:


bin(mu.reg_read(UC_ARM64_REG_V0))


# In[ ]:




